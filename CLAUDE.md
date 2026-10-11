# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A Python job that logs into the NYC DEP "My DEP Account" portal (`a826-umax.dep.nyc.gov`) with Selenium + headless Chrome, downloads the daily meter readings, and emails them over SMTP. It runs nightly as a scheduled GitHub Actions workflow (`.github/workflows/dep.yml`, 22:00 UTC, also `workflow_dispatch`). Credentials are repo secrets (`DEP_USER`, `DEP_PWD`, `SMTP_*`, `MAIL_FROM`, `MAIL_TO`), mapped to the env vars the code reads.

## Commands

- Setup: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`. Chrome must be installed; Selenium 4 fetches its own driver.
- Run: `.venv/bin/python main.py`. Needs a gitignored `.env` with `user`, `pwd` (DEP login) and `LOCAL=1`. Without `SMTP_HOST` the email is printed, not sent.
- Tests: `.venv/bin/python -m unittest discover -s test -p "test_format.py"` (any pattern). Use `discover -s test`, not `-m unittest test.xxx`: `test` resolves to the stdlib package. `test_format.py` and `test_daily_formatter.py` are offline; `testscrape.py` logs in to the live site.

## Architecture

Flat module layout at the repo root; `main.py` orchestrates:

- `scrape.py` — `Session` context manager starts headless Chrome and logs in through the Azure AD B2C redirect (`signInName` / `password` / `next`). `export_csv(tab)` clicks the `NavMenu_Usage` / `NavMenu_Billing` tab, waits for the page's data text (`LOADED_TEXT`), clicks "Export displayed data to Excel" (which downloads a CSV into a temp dir) and parses it. The charts are SVG with no tables, so the CSV export is the data source. `scrape_daily_usage()` (Usage export, current month) and `scrape_monthly()` (Billing export) wrap this. `format_daily_usage` and `parse_csv` are pure and unit-tested.
- `format.py` — turns billing CSV rows into fixed-width text tables (`format_bills`, `format_reads`).
- `aws.py` — storage/notification layer (name is historical). With `LOCAL=1` (always set in the workflow) it skips boto3: `put_text` writes to `data/`, and `send` / `send_daily` email over SMTP via `local_notify` if `SMTP_HOST` is set (needs `SMTP_USER`, `SMTP_PASSWORD`, `MAIL_FROM`, `MAIL_TO`; port 587 STARTTLS), else print. Without `LOCAL` it uses the old S3 bucket `dep-history` and SNS topic, which boto3 (not in `requirements.txt`) would need.
- `main.py` — `daily()` (daily readings → `daily_reads.txt` → email) and `monthly()` (billing history → `reads.txt` / `bills.txt` → one email). The `__main__` block runs only `daily()`. Calls `load_dotenv()` first.

## Gotchas

- The new site has no separate monthly meter-reads history, so `monthly()`'s "reads" are billed HCF per bill period from the same Billing export as the amounts.
- Scraping depends on element IDs (`NavMenu_*`, the B2C login IDs) and the export button text. If the site changes again, check those first. The old host `a826-amr.nyc.gov` no longer exists.
- The old AWS hosting (ECS/Batch container, S3 history, SNS emails) has been torn down. `aws.py` still contains the S3/SNS code path for when `LOCAL` is unset, but it is unused and nothing in AWS backs it any more.
