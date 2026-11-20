# AgenticQuantF

This is a place where I find all the quant roles and jobs that are getting transitioned into Agentic based ones and this place acts as a repo that has all the projects that are highly demanded in the new era go agentic quant analyst.

---

## Agentic job-application pipeline

A command-line workflow that **finds jobs in any field, scores your fit honestly, builds a tailored CV and cover letter for each job you choose, and then applies on your behalf only after you have reviewed and signed off**. You stay in control at every step; the agent only does the tedious parts.

```
scan  ──►  scanned_jobs.xlsx  ──►  (you tick Approve)  ──►  approve  ──►  approved_jobs.xlsx + one folder per job
                                                                                   │
                         submitted  ◄──  apply  ◄──  (you read the pack, then  review --ok)  ◄──┘
```

* **Any topic, one sentence:** `./jf scan cyber security internships`, `./jf scan quantum computing graduate roles`, `./jf scan applied AI internships`. A topic means the *whole field* (cyber security finds software, AI/LLM, cloud, system security…; applied AI also finds ML engineer, ML researcher, AI researcher…).
* **Honest, evidence-based fit score:** an LLM reads each full job description against *your* profile, lists the requirements and quotes your evidence for each. Hard requirements you fail (PhD-only, citizenship…) are flagged and skipped.
* **Two Excel files, two human gates:** you approve which jobs get an application, and you sign off each tailored CV and cover letter before anything is sent.
* **A CV that cannot invent facts:** the CV is tailored by *choosing and ordering your own bullets* and is checked line by line against your profile. Anything it cannot verify is discarded and the reason is written to a change log.
* **One folder per job** with everything: job description, fit analysis, CV (PDF + editable source), change log, cover letter, apply log.

> Built on the open-source [`job-finder-ai`](https://github.com/AkhilBaja3005/job-finder) (MIT, by Akhil Baja), vendored in `job-finder-src/`, with the scan/approve/prepare/review/apply workflow, Excel trackers, field-wide topic search, evidence-based scoring and CV/cover-letter packs added on top. See `job-finder-src/LICENSE`.

---

## 1. Requirements

| | |
|---|---|
| Python | 3.10 or newer |
| OS | macOS or Linux (Windows: use WSL) |
| Gemini API key | free key from <https://aistudio.google.com/apikey> (used for scoring, tailoring, cover letters and the form-filling agent) |
| Your resume | a PDF (used as a fallback and with `--no-pack`) |
| Disk / browser | `setup.sh` installs a headless Chromium (~150 MB) used to read job pages and render PDFs. **No LaTeX needed.** |

## 2. Setup (about 5 minutes)

```bash
git clone https://github.com/lokesMCI/AgenticQuantF.git
cd AgenticQuantF
./setup.sh                  # creates .venv, installs everything, installs Chromium, creates .env + candidate_profile.json
```

Then fill in the two private files that `setup.sh` created (both are git-ignored and never leave your machine except what is sent to Gemini, see *Privacy*):

1. **`.env`**: set `GEMINI_API_KEY` and `MASTER_RESUME_PATH=/full/path/to/your_resume.pdf`. Everything else is optional (see comments in `.env.example`).
2. **`candidate_profile.json`**: replace the example with **your** details: contact info, work-eligibility facts (citizenship, sponsorship), education, experience (with bullet points), projects, skills, and the `search_preferences` block (topics, level, locations, time window).
   *The profile is the single source of truth: the CV and cover letters can only use what is written here, so put your real achievements (with numbers) in it.*

```bash
./jf doctor                 # health check: every line should say ok (warn lines are optional)
./jf profile --show         # re-read your profile once and make sure it is all true
./jf ats                    # optional: resume health audit (what your target roles expect vs what your profile shows)
./jf ats --add-skills       # optional: add skills your profile evidences but does not list (asks first, makes a backup)
```

All commands go through the launcher **`./jf`** (it always uses this folder for config, data and outputs, wherever you run it from). `./jf --help` lists everything.

---

## 3. The workflow, step by step

### Step 1: Search: `./jf scan`

```bash
./jf scan                                       # your saved defaults (profile: topics + level + locations)
./jf scan cyber security internships            # plain words; level word (intern/graduate/junior/senior) is picked out
./jf scan --topic "applied AI, cyber security" --level intern
./jf scan quantum computing graduate roles --timeframe 1m --location "Manchester, UK"
```

What happens:

1. **Topic → field map** (once per topic, cached in `data/topic_terms.json`): the LLM lists title words for every sub-area (`include`), look-alikes to drop (`exclude`, e.g. *security guard*) and extra board searches (`search`). Inspect or rebuild it with `./jf topic cyber security [--refresh]`; edit the JSON by hand to tune it.
2. **Search** across LinkedIn, Indeed, Jobserve, Greenhouse/Lever/Ashby/Workday/BambooHR company boards and more, using the topic plus the sub-area searches.
3. **Filter** on the *title*: must fit the field, carry a level word, and not be senior (for intern/graduate searches). Every scan prints a sample of what it dropped and why.
4. **Score** each survivor against your profile (section 5) and look for a **closing date** (job text, page metadata, or a quoted deadline).
5. **Save** everything new to `applications_tracker/scanned_jobs.xlsx`. Nothing is applied to.

Useful options: `--limit 20`, `--min-ats 70`, `--loose` (also read descriptions), `--exact` (only your own words), `--no-ai-score`, `--no-enrich`, `--sponsor-only`, `--timeframe 24h|1w|1m`, `--skip-portals none`. See `./jf scan --help`.

**`./jf scan ... --dry-run`** is a search-only test: it writes nothing and scores nothing, and prints the whole funnel (postings found per source, how many each stage removed, and *every* removed title with its reason). Use it whenever the number of saved jobs surprises you.

> **Why "130 found" can become 15 saved:** "found" counts everything every source returned. Job boards like Jobserve and Indeed ignore "Intern" and return permanent roles, which the level filter removes; jobs already in your tracker are skipped; off-topic titles are dropped. Real internships come mostly from LinkedIn. **Internships stay open for weeks, so use a month window (`--timeframe 1m`, or `timeframe` in your profile) for the first scans** (a one-week window found 1 new applied-AI internship, a month found about 20).

### Step 2: Review in Excel and approve

```bash
./jf open            # opens scanned_jobs.xlsx
```

Sort and filter freely. On the jobs you want, set **Approve = Yes** (dropdown), save and close the file, then:

```bash
./jf approve                       # moves exactly the ticked rows into approved_jobs.xlsx
./jf approve --ids 3,7             # or approve by ID without touching Excel
./jf approve --min-ats 85          # or every open row scoring at least 85
./jf approve --revoke --ids 7      # take one back out (unless already applied)
./jf approve --list                # what is waiting
```

Rows that cannot be applied to are refused with a reason (already applied, you fail a hard requirement, closing date passed, no URL).

### Step 3: Application packs: built automatically by `approve`

For every newly approved job, one folder under `applications/` is created (details in section 4):

* the **job description** is saved,
* the **CV is tailored** to the job (reordered/trimmed from *your own* bullets, with a line-by-line change log and a keyword before/after table),
* a **cover letter is written only if the posting asks for one** (`--cover-letter always|never` to force),
* a **`REVIEW.md` checklist** tells you what to check.

```bash
./jf prepare --ids 3                  # (re)build a pack; keeps your edits to cv.json / cover_letter.txt
./jf prepare --ids 3 --redo           # regenerate from scratch
./jf prepare --ids 3 --render-only    # rebuild the PDFs after you edited cv.json / cover_letter.txt (no LLM call)
```

### Step 4: Review and sign off (manual, required)

```bash
./jf review                  # list packs and whether you signed them off
./jf review --open 3         # open that job's folder
#   read REVIEW.md, cv.pdf, cv_changes.md, cover_letter.txt; edit cv.json / cover_letter.txt if you want
./jf review --ok 3           # "I reviewed these documents": allows apply to use them (Docs OK = Yes)
```

Any regeneration or re-render resets the sign-off, so you always approve the documents that will actually be sent.

### Step 5: Apply

```bash
./jf apply --dry-run --limit 1       # PREVIEW: opens the form, fills it in, STOPS before Submit. Start here.
./jf apply --submit                  # really submits every signed-off job (shows the list, asks y/N)
./jf apply --submit --ids 3          # just one
./jf apply --retry --submit          # also retry rows that ended in Needs Review
./jf apply "<job url>" --submit      # one job outside the queue
```

`apply` reads **only `approved_jobs.xlsx`**, and only rows with **Docs OK = Yes**. For each job it uploads **that pack's `cv.pdf`**, pastes **that pack's reviewed `cover_letter.txt` verbatim** (the agent is forbidden from writing its own), then records the result in **both** workbooks and in the job's `apply_log.md`:

| Outcome | Status | Meaning |
|---|---|---|
| Submission confirmed | **Applied** | the confirmation page/text was detected |
| CAPTCHA / login wall / unclear result / error | **Needs Review** | reason in *Notes*; a screenshot is copied into the pack |
| Posting removed | **Closed** | |
| Preview run | unchanged | a dated note is added; nothing is marked Applied |

Safety nets: a missing resume file stops the run before any browser opens; applied/skipped/closed jobs (also if *you* mark them in the scanned file) are never applied to again.

---

## 4. Files and folders the tool generates

```
AgenticQuantF/                      (your working folder; everything below marked "private" is git-ignored)
├── README.md  jf  setup.sh  .env.example  candidate_profile.example.json  LICENSE      committed
├── job-finder-src/                                                                       committed: the application code
│
├── .env                                  private: API keys and settings
├── candidate_profile.json                private: YOUR profile = the single source of truth for CV / letters / scoring
│
├── applications_tracker/
│   ├── scanned_jobs.xlsx                 private: EVERYTHING `scan` found (you review here, tick Approve)
│   └── approved_jobs.xlsx                private: the queue `apply` reads (only jobs you approved)
│
├── applications/                         private: ONE FOLDER PER APPROVED JOB
│   └── 0007_acme-ltd_applied-ai-intern/
│       ├── REVIEW.md                     what to check, in order, plus any warnings
│       ├── job.md                        link, location, closing date, scores, why it fits
│       ├── job_description.txt           the full posting text (saved so it cannot disappear)
│       ├── fit_analysis.md               each requirement: met / partial / NOT met, with your evidence
│       ├── cv.pdf                        the tailored CV that will be UPLOADED
│       ├── cv.json  cv.html              editable source of cv.pdf (edit cv.json, then `prepare --render-only`)
│       ├── cv_changes.md                 exactly what changed vs your profile, keyword coverage before/after, gaps
│       ├── cover_letter.txt              only if the job asks for one: pasted VERBATIM into the form
│       ├── cover_letter.pdf              the same letter as a file, for forms that want an upload
│       ├── cover_letter_notes.md         validator warnings, requirements you cannot evidence, alternative openings
│       ├── apply_log.md                  added by `apply`: every preview/submit with time, result, screenshot
│       ├── screenshot_*.png              added by `apply` when the agent stops for review
│       └── manifest.json                 machine-readable summary
│
└── data/                                 private caches (safe to delete)
    ├── topic_terms.json                  the field map per topic: EDITABLE (include / exclude / search)
    ├── fit_cache.db                      cached fit analyses (stable scores, no repeat LLM calls)
    └── jd_cache.db …                     cached job pages
```

**`scanned_jobs.xlsx` / `approved_jobs.xlsx` columns:** ID · Company · Job Role · Location · Platform · Posted · **Closing Date** · **Applied** · **Status** · **Approve** · ATS % · Skills % · Experience % · Role Fit % · **Scored By** · Matched / Missing Skills · **Fit Summary** · UK Sponsor · Level · Salary · Date Found / Applied · **Notes** · **Docs OK** · **Cover Letter** · **Pack Folder** · Job URL.
Statuses: New → **Approved** → **Applied** (or Needs Review / Closed) · also Shortlisted, Interview, Offer, Rejected, Skipped, Withdrawn. Row colours: green = applied, blue = approved, orange = closes within 7 days, grey = closed. Save and close the file in Excel before running `approve`/`apply`.

---

## 5. How scoring works (and why it is not "keyword matching")

No real ATS gives candidates a number, so this is an **evidence-based fit estimate**, not a prediction of one vendor's system.

* The LLM reads the **full job description** and lists its real requirements (any field, no fixed skill list). Each is marked **met / partial / not met** against your profile **with your evidence quoted**. The numbers are plain arithmetic over those verdicts (must-haves count 3× nice-to-haves), so they are explainable and cached/stable.
* **Hard requirements** (citizenship, clearance, "must be enrolled in a PhD", "must not already hold a degree"…) give **0% and Status = Skipped**; a missing *degree-level* requirement caps the score at 50.
* **Scored By** shows the engine: `AI` (full analysis), `Keyword` (fixed-list fallback if the LLM was unavailable) or `Listing estimate` (no description could be fetched).
* `./jf ats --jd-url "<link>"` explains the score for one job requirement by requirement.

### How the CV is tailored without inventing anything

The model never writes a free-form CV. It returns a **plan over your existing material** (which bullets to keep and in what order, how to order your skills, a retargeted summary, a few optional rewordings, the job's key terms). Code then verifies it, and anything unverifiable is thrown away:

* roles, companies, dates and degrees are copied untouched; every role keeps at least one bullet,
* a summary or reworded bullet may only use **numbers and tool names that already exist in your profile**, must keep the original's numbers/headline proof, may only use **words your profile already uses**, and may not contain marketing filler ("passionate", "highly motivated"…) or **job keywords you have no evidence for**,
* a skill is shown only if your profile mentions it,
* if the first plan has problems the model is told exactly what was wrong and gets **one** retry; what still fails is dropped and your original wording stays.

`cv_changes.md` lists every change, every rejected suggestion, and the job keywords you do **not** have evidence for (shown as gaps; never added). The CV is a single-column, text-based PDF (an ATS can read it) that is tightened automatically to fit one page. Cover letters use a separate generator with a fact-checker (length, clichés, placeholders, numbers not in your profile) and a plain factual fallback.

---

## 6. Privacy and safety

* **Never committed:** `.env`, `candidate_profile.json`, both Excel files, `applications/`, `data/`, virtualenvs (whitelist `.gitignore`). Check with `git status` before any push.
* **Sent to Google Gemini:** job descriptions, and from your profile only skills, experience, education, projects and work-eligibility facts. **Never** contact details, passwords, or gender/ethnicity/veteran/disability fields (those are used only by the form-filling agent on the application page itself).
* **Submitting is irreversible.** Always start with `./jf apply --dry-run --limit 1` and watch the browser. The agent types your real details into real forms and may create an account on a job portal using `PORTALS_PASSWORD` (use a throwaway password). Skim the first few applications' screening answers.
* `JOB_FINDER_DISABLE_GUARDRAILS=0` (default) keeps a safety stop at the review step. Respect the terms of the job sites you use; job boards may block or rate-limit automated access.
* Gemini free keys are rate-limited; scans still finish (scoring falls back to the keyword engine and says so in *Scored By*). Add more comma-separated keys in `GEMINI_API_KEY` to spread load.

## 7. Command cheat sheet

```bash
./jf doctor                                   # health check
./jf topic cyber security                     # what a topic covers (--refresh to rebuild)
./jf scan cyber security internships          # 1. find + score jobs  -> scanned_jobs.xlsx
./jf open                                     # 2. review in Excel, tick Approve = Yes
./jf approve                                  # 3. queue them + build packs (CV, cover letter, notes)
./jf review --open 3  &&  ./jf review --ok 3  # 4. read the pack, then sign off
./jf apply --dry-run --limit 1                # 5. preview one form
./jf apply --submit                           #    send the signed-off applications
./jf tracker --approved                       # status in the terminal
./jf ats --jd-url "<link>"                    # why this score?
```

## 8. Troubleshooting

| Symptom | Fix |
|---|---|
| `No virtual environment found` | run `./setup.sh` |
| `Nothing approved to apply to` | tick **Approve = Yes** in `scanned_jobs.xlsx`, then `./jf approve` |
| `documents not signed off` | `./jf review --open <ID>`, read the pack, then `./jf review --ok <ID>` |
| `no application pack yet` | `./jf prepare --ids <ID>` (or `apply --no-pack` to use your master resume) |
| scan finds 0 jobs, many "off topic" | read the *Dropped* list it prints; widen with `--timeframe 1m`, commas for alternatives, `--loose`, or edit `data/topic_terms.json` |
| CV is 2 pages | trim bullets in `cv.json`, then `./jf prepare --ids <ID> --render-only` |
| `Cannot write …xlsx` | close the file in Excel and retry |
| Gemini `429 quota` | wait, or add another key; cached results are not recomputed |
| anything else | add `--debug`; logs are in `~/.job-finder/logs/job-finder.log` |

## 9. Development

```bash
.venv/bin/python -m pytest job-finder-src/tests/test_excel_tracker.py job-finder-src/tests/test_approval.py \
  job-finder-src/tests/test_scan_apply_flow.py job-finder-src/tests/test_role_spec.py job-finder-src/tests/test_fit_scorer.py \
  job-finder-src/tests/test_resume_audit.py job-finder-src/tests/test_cv_tailor.py job-finder-src/tests/test_application_pack.py
```
These tests are offline (the LLM, job boards and browser agent are mocked; one test renders a real PDF with Chromium and skips if it is unavailable). Other test files in `job-finder-src/tests/` come from the upstream project and need network access and API keys.

Key modules (all under `job-finder-src/`): `backend/services/` · `role_spec.py` (topics → searches + title filter) · `fit_scorer.py` (evidence-based scoring) · `excel_tracker.py` · `approval.py` · `cv_tailor.py` · `application_pack.py` · `resume_audit.py` · `closing_date.py`; commands in `job_finder/commands/` (`scan`, `approve`, `prepare`, `review`, `apply`, `topic`, `ats`, `open`).

## License

MIT. See `LICENSE` (this repository) and `job-finder-src/LICENSE` (upstream project).
