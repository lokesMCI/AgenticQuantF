"""`job-finder scan` command: discover jobs and save them to the Excel tracker. Never applies."""

import argparse
import logging
import sys

from job_finder import ui

logger = logging.getLogger(__name__)


def run(args: argparse.Namespace):
    request = " ".join(args.request or []).strip()
    if request.lower().startswith(("http://", "https://")) or args.retired_apply_flag or args.retired_apply_opt:
        ui.error("`scan` only discovers jobs now; it no longer tailors resumes or applies.")
        ui.info("Run `job-finder scan` to fill the Excel tracker, then `job-finder apply` (or `apply <url>`) to apply.")
        sys.exit(2)

    try:
        from backend.services.role_spec import normalize_level
        normalize_level(args.level)  # fail fast, before any searching, on a typo like --level interm
    except ValueError as ve:
        ui.error(str(ve))
        sys.exit(2)

    import asyncio
    from applications_tracker.scheduled_job_scanner import run_scan

    # Refresh the verified ATS company-board registry if requested or stale (>24h)
    try:
        try:
            from backend.services.company_slug_registry import get_active_slugs, validate_all_unverified_slugs, should_run_daily_harvest
            from backend.services.company_slug_harvester import harvest_all_company_slugs
        except ImportError:
            from services.company_slug_registry import get_active_slugs, validate_all_unverified_slugs, should_run_daily_harvest
            from services.company_slug_harvester import harvest_all_company_slugs

        if getattr(args, "harvest", False) or should_run_daily_harvest(max_age_hours=24.0):
            print("[ATS Harvester] Running scheduled daily refresh of verified ATS company boards...")
            asyncio.run(harvest_all_company_slugs(sources=["seeds"]))
            asyncio.run(validate_all_unverified_slugs(limit=50))
            active = get_active_slugs()
            total_active = sum(len(slugs) for slugs in active.values())
            print(f"  Active ATS boards ready: {total_active} companies across Ashby, Greenhouse, Lever\n")
    except Exception as he:
        logger.debug(f"Harvester init note: {he}")

    asyncio.run(run_scan(
        role=args.role,
        location_override=args.location,
        timeframe_override=args.timeframe,
        min_ats=args.min_ats,
        limit=args.limit if args.limit > 0 else None,
        skip_portals=args.skip_portals,
        sponsor_only=True if args.sponsor_only else None,
        top_applicant_only=True if args.top_applicant else None,
        headless=True if args.headless else None,
        enrich=not args.no_enrich,
        topic=args.topic,
        level=args.level,
        request=request or None,
        loose=args.loose,
        exact=args.exact,
        ai_score=not args.no_ai_score,
        dry_run=args.dry_run,
    ))
