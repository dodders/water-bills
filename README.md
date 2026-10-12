# water-bills

Logs into the NYC DEP "My DEP Account" portal, pulls the daily meter readings, and emails them. Runs nightly as a scheduled GitHub Actions workflow.

## How it works

`main.py` uses Selenium + headless Chrome to sign in (the portal redirects through an Azure B2C login), opens the Usage tab, and downloads the "Export displayed data to Excel" CSV. The rows are formatted into a plain-text summary and emailed over SMTP.

## Hosting

`.github/workflows/dep.yml` runs `main.py` nightly (22:00 UTC) and can be started by hand from the Actions tab. It uploads the generated `data/*.txt` files as a workflow artifact (kept 90 days). A failed run emails the repo owner via GitHub.

Repo secrets (Settings → Secrets and variables → Actions):

| Secret | Purpose |
|---|---|
| `DEP_USER`, `DEP_PWD` | DEP login |
| `SMTP_HOST`, `SMTP_USER`, `SMTP_PASSWORD` | SMTP server (for Gmail use `smtp.gmail.com` and an [app password](https://myaccount.google.com/apppasswords)) |
| `MAIL_FROM`, `MAIL_TO` | sender and comma-separated recipients |

## Running locally

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

Create a gitignored `.env`:

```
user=<DEP login>
pwd=<DEP password>
```

then `.venv/bin/python main.py`. Without the `SMTP_*` / `MAIL_*` variables the email is printed instead of sent. Requires Chrome; Selenium fetches the driver.

Tests: `.venv/bin/python -m unittest discover -s test -p "test_*.py"` (`testscrape.py` logs in to the live site and needs `.env`).

## Infrastructure history

Until October 2026 this ran as a container on AWS (us-east-1): an EventBridge rule (`dep-daily`) launched an ECS Fargate task from an ECR image, history files were kept in the S3 bucket `dep-history` (versioned), config in `dep-config`, and results were emailed through the SNS topic `dep-notifications`. A Batch queue, compute environment and job definitions (`dep`) existed as an earlier hosting attempt. An unapplied Terraform version of the ECS setup was also in this repo.

All of it was removed on 2026-10-11/12, along with the IAM users `dep` and `dep-admin` (and their access keys) and the group `dep-group`. Nothing in AWS is used any more. The S3 history (3 files and 1,121 old versions, 2018–2021) and the config file were downloaded first and kept outside the repo. The IAM user `iam-admin` (the old Terraform profile, full admin) was deliberately left in place.

The portal itself changed in March 2024: the old `a826-amr.nyc.gov` site was replaced by `a826-umax.dep.nyc.gov`, which is what broke the original scraper.

