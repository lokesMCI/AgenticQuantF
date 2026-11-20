"""
Application history tracking — records which jobs a user has tailored a
resume for or applied to, so that history survives a page refresh/browser
close (previously nothing persisted this at all).

Supabase-backed (an `applications` table) when configured, matching the
existing user_resumes persistence pattern in auth.py/main.py. Otherwise the
local ledger is the Excel tracker (see excel_tracker.py), shared with the
`scan` and `apply` commands.
"""

import json
import os
import re
import time
import hashlib
from datetime import datetime, timezone
from typing import Optional, Any, Dict, List, Tuple
try:
    # pyrefly: ignore [missing-import]
    from services.auth import supabase_request, get_user_by_token
except ImportError:
    def supabase_request(*args: Any, **kwargs: Any) -> Any: return None
    def get_user_by_token(*args: Any, **kwargs: Any) -> Any: return None
# pyrefly: ignore [missing-import]
from config.constants import get_output_dir, resolve_workspace_root
try:
    from services.excel_tracker import ExcelTracker, record_from_payload
except ImportError:
    from backend.services.excel_tracker import ExcelTracker, record_from_payload

BASE_DIR = resolve_workspace_root()
OUTPUT_DIR = get_output_dir()


# Cap on entries kept in the local JSON fallback file and Supabase query limit.
# Increased from 200 to 5000 so users with extensive application history (1000+ entries) see their full history.
MAX_LOCAL_HISTORY_ENTRIES = 5000


def _safe_key(token: Any) -> str:
    """Mirrors session_store's _safe_key(): filesystem-safe per-user cache key."""
    if token is None:
        return "guest"
    key = str(token).strip()
    key = re.sub(r'[^a-zA-Z0-9_-]', '', key)[:40]
    return key or "guest"


def _read_local_history(token: Optional[str]) -> list[dict]:
    """Local application history = the Excel tracker's rows, in the legacy dict shape."""
    try:
        return ExcelTracker().legacy_entries()
    except Exception as e:
        print(f"[application_tracker] Failed to read Excel tracker: {e}")
        return []


def _record_local(record: dict) -> None:
    """Add a job to the Excel tracker, or update its status if the job is already tracked."""
    try:
        tracker = ExcelTracker()
        rec = record_from_payload({
            "company": record.get("company"), "job_title": record.get("job_title"),
            "job_url": record.get("job_url"), "score": record.get("score"),
            "status": record.get("status"), "platform": record.get("source_mode"),
            "notes": record.get("notes"),
        })
        added, _ = tracker.add_jobs([rec])
        if not added and record.get("job_url") and record.get("status"):
            tracker.update(url=record["job_url"], status=record["status"])
    except Exception as e:
        print(f"[application_tracker] Failed to write Excel tracker: {e}")


def record_application(token: Optional[str], entry: dict) -> None:
    """
    Records one history entry. `entry` is expected to have:
    job_title, company, job_url, score (optional), status ('tailored'|'applied').
    Adds a server-side timestamp so the client can't spoof ordering.
    """
    record = {**entry, "timestamp": time.time()}

    user = get_user_by_token(token) if token else None
    if user and user.get("id"):
        # supabase_request() never raises — it catches every exception itself
        # (auth.py) and returns []. So the only success signal available here
        # is a non-empty response (POST with Prefer: return=representation
        # returns the inserted row(s) on success). Treating "no exception" as
        # success meant a POST that silently failed (bad column type, RLS
        # rejection, etc.) never fell through to the local-file fallback below
        # — the write looked like it worked and the entry was just lost.
        supa_payload = {
            "user_id": user["id"],
            "job_title": record.get("job_title", "") or "Target Role",
            "company": record.get("company", "") or "Hiring Company",
            "job_url": record.get("job_url", ""),
            "score": record.get("score"),
            "status": record.get("status", "tailored"),
            "created_at": datetime.fromtimestamp(record["timestamp"], tz=timezone.utc).isoformat(),
        }
        if record.get("source_mode"):
            supa_payload["source_mode"] = record.get("source_mode")
        if record.get("recruiter_name"):
            supa_payload["recruiter_name"] = record.get("recruiter_name")
        if record.get("recruiter_profile_url"):
            supa_payload["recruiter_profile_url"] = record.get("recruiter_profile_url")
        if record.get("overleaf_url"):
            supa_payload["overleaf_url"] = record.get("overleaf_url")
        if record.get("pdf_url"):
            supa_payload["pdf_url"] = record.get("pdf_url")

        result = supabase_request("applications", "POST", supa_payload)
        if result:
            return
        print("[application_tracker] Supabase write returned no rows, falling back to local file")

    # Local snapshot persistence
    pdf_p = record.get("pdf_path")
    if pdf_p and isinstance(pdf_p, str) and os.path.exists(pdf_p):
        try:
            snapshot_dir = os.path.join(OUTPUT_DIR, _safe_key(token), "snapshots")
            os.makedirs(snapshot_dir, exist_ok=True)
            job_t = str(record.get("job_title") or "")
            app_id = f"{int(record['timestamp'])}_{hashlib.md5(job_t.encode('utf-8')).hexdigest()[:6]}"
            snap_pdf = os.path.join(snapshot_dir, f"tailored_{app_id}.pdf")
            import shutil
            shutil.copy2(pdf_p, snap_pdf)
            record["snapshot_pdf_path"] = snap_pdf
        except Exception as snap_err:
            print(f"[application_tracker] Warning: Could not create PDF snapshot: {snap_err}")

    _record_local(record)


def update_application_status(
    token: Optional[str],
    job_url: str,
    new_status: str,
    job_title: Optional[str] = None,
    company: Optional[str] = None,
    score: Optional[int] = None
) -> bool:
    """Updates status ('applied'|'autofilled'|'tailored'|'saved') for a job URL, creating a record if needed."""
    user = get_user_by_token(token) if token else None
    if user and user.get("id"):
        result = supabase_request(
            f"applications?user_id=eq.{user['id']}&job_url=eq.{job_url}",
            "PATCH",
            {"status": new_status}
        )
        if result:
            return True
        # If record didn't exist in Supabase, insert it
        if job_title or company:
            record_application(token, {
                "job_title": job_title or "Target Role",
                "company": company or "Hiring Company",
                "job_url": job_url,
                "score": score,
                "status": new_status,
                "source_mode": "discovery"
            })
            return True

    # Fallback to the local Excel tracker
    try:
        if job_url and ExcelTracker().update(url=job_url, status=new_status):
            return True
    except Exception as e:
        print(f"[application_tracker] Failed to update Excel tracker: {e}")
    if job_title or company or job_url:
        record_application(token, {
            "job_title": job_title or "Target Role",
            "company": company or "Hiring Company",
            "job_url": job_url,
            "score": score,
            "status": new_status,
            "source_mode": "discovery"
        })
        return True
    return False


def list_applications(token: Optional[str] = None) -> list[dict]:
    """Returns history entries newest-first."""
    user = get_user_by_token(token) if token else None
    if user and user.get("id"):
        rows = supabase_request(
            f"applications?user_id=eq.{user['id']}&order=created_at.desc&limit={MAX_LOCAL_HISTORY_ENTRIES}",
            "GET",
        )
        if isinstance(rows, list):
            return [
                {
                    "job_title": r.get("job_title", ""),
                    "company": r.get("company", ""),
                    "job_url": r.get("job_url", ""),
                    "score": r.get("score"),
                    "status": r.get("status", "tailored"),
                    "recruiter_name": r.get("recruiter_name"),
                    "recruiter_profile_url": r.get("recruiter_profile_url"),
                    "overleaf_url": r.get("overleaf_url"),
                    "pdf_url": r.get("pdf_url"),
                    "source_mode": r.get("source_mode", "website"),
                    "timestamp": datetime.fromisoformat(r["created_at"]).timestamp() if r.get("created_at") else None,
                }
                for r in rows
                if isinstance(r, dict)
            ]

    entries = _read_local_history(token)
    return sorted(entries, key=lambda e: e.get("timestamp", 0), reverse=True)
