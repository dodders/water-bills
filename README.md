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
