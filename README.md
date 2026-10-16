# Reddit Community Trends Analyzer

A small, **read-only**, manually executed Python prototype for personal, non-commercial analysis of public discussions in selected cryptocurrency and Web3 subreddits.

**Status:** Initial prototype; API access has not been granted or tested. Do not run against Reddit until Reddit has explicitly authorized your API use. This repository does not imply Reddit endorsement.

## What it does

- Retrieves a configurable, small sample of recent public posts from selected subreddits.
- Retrieves limited top-level comment metadata (timestamp and score only); it does **not** store comment text or usernames.
- Generates local CSV files containing post title, timestamp, score and comment count, plus aggregated title-word frequencies.
- Does not post, comment, vote, send messages, or interact with users.
- Does not train AI models or perform individual-user profiling.

## Requirements

- Python 3.10+
- Explicit Reddit API authorization and valid credentials for a permitted script-type application.

## Setup

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # On Windows, copy manually or use: copy .env.example .env
```

Edit `.env` locally with your authorized Reddit API credentials and account details. **Never commit `.env` or share credentials.**

## Run (only after authorization)

```bash
python main.py --subreddits CryptoCurrency,ethereum --limit 5 --comments-per-post 5
```

Outputs are written to `reports/` (ignored by Git). The script does not run on a schedule and makes no write requests. Do not use it for mass collection or scraping.

## Data handling and limitations

- Local report files are **not** automatically updated when Reddit posts are edited or deleted. Delete reports promptly when no longer necessary, and implement deletion reconciliation before any ongoing or expanded use, consistent with Reddit's applicable requirements.
- The script avoids collecting usernames and comment bodies but retains post titles and timestamps. Post titles may still contain personal information; review output accordingly.
- Respect Reddit's API terms, rate limits, content deletion obligations, subreddit rules and any authorization-specific restrictions.
- If API access is denied, do not bypass restrictions through scraping or alternative credentials.
- The tool is a basic prototype, not a validated sentiment-analysis or research instrument. Keyword counts are descriptive and may be misleading.

## Why an external script?

This prototype is designed for local Python processing and offline CSV summaries, rather than an interactive Reddit-hosted application. The suitability of Devvit versus traditional API access remains subject to Reddit's assessment.

## License

MIT (see LICENSE).
