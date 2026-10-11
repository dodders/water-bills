# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A Python job that logs into the NYC DEP "My DEP Account" portal (`a826-umax.dep.nyc.gov`) with Selenium + headless Chrome, pulls water usage / billing data, writes it to S3 (or `data/` locally), and emails it via an SNS topic. The intended hosting is a Docker container on AWS (ECS Fargate, `terraform/`), but the Docker/Terraform/Pipfile setup has not been updated for the new portal (see Gotchas).

## Commands

- Setup (local): `python3 -m venv .venv && .venv/bin/pip install selenium python-dotenv requests beautifulsoup4 boto3`. Chrome must be installed; Selenium 4 fetches its own driver.
- Run: `.venv/bin/python main.py`. Needs a gitignored `.env` with `user` and `pwd` (DEP login, an email address). Add `LOCAL=1` to skip AWS (see below); otherwise AWS credentials are required.
- Tests: `.venv/bin/python -m unittest discover -s test -p "test_format.py"` (any pattern works). Use `discover -s test`, not `-m unittest test.xxx`, because `test` resolves to the stdlib package. `test_format.py` and `test_daily_formatter.py` are offline; `testscrape.py`, `test_aws.py` and `test_email.py` hit the live site / AWS and some are stale.
- Docker/infra (legacy, untested against the new portal): `make build|rund|shell|deploy`, `scripts/docker-*.sh`, `terraform/`.

## Architecture

Flat module layout at the repo root; `main.py` orchestrates:

- `scrape.py` — `Session` context manager starts headless Chrome and logs in through the Azure AD B2C redirect (`signInName` / `password` / `next`). `export_csv(tab)` clicks the `NavMenu_Usage` / `NavMenu_Billing` tab, waits for the page's data text (`LOADED_TEXT`), clicks "Export displayed data to Excel" (which downloads a CSV into a temp dir) and parses it. The charts are SVG with no tables, so the CSV export is the data source. `scrape_daily_usage()` (Usage export, current month) and `scrape_monthly()` (Billing export) wrap this. `format_daily_usage` and `parse_csv` are pure and unit-tested.
- `format.py` — turns billing CSV rows into fixed-width text tables (`format_bills`, `format_reads`).
- `aws.py` — S3 + SNS. With `LOCAL=1` it skips boto3 entirely: `put_text` writes to `data/` and `send` / `send_daily` print the email instead of sending. Otherwise it writes to the `dep-history` bucket (same key each run; use S3 versioning for history) and publishes to the hard-coded `dep-notifications` SNS topic ARN.
- `main.py` — `daily()` (daily readings → `daily_reads.txt` → email) and `monthly()` (billing history → `reads.txt` / `bills.txt` → one email). The `__main__` block runs only `daily()`. Calls `load_dotenv()` first.

## Gotchas

- The new site has no separate monthly meter-reads history, so `monthly()`'s "reads" are billed HCF per bill period from the same Billing export as the amounts.
- Scraping depends on element IDs (`NavMenu_*`, the B2C login IDs) and the export button text. If the site changes again, check those first. The old host `a826-amr.nyc.gov` no longer exists.
- The `Dockerfile` and `Pipfile` still target Python 3.6, the old `chromedriver` setup and the old Selenium API; they need updating before the container will work. The README is also stale.
- `utils.py` is an unfinished stub.
