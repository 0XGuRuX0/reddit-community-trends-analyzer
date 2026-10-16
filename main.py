"""Read-only, manually triggered Reddit community trend report."""
import argparse
import csv
import os
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import praw
from dotenv import load_dotenv

DEFAULT_SUBREDDITS = "CryptoCurrency,ethereum,ethfinance,solana"
STOPWORDS = set('the and for with this that from have are was were you your they them about into just not but can has had its our out what when where why how who all any more than then there their would should could will one two post posts reddit comments comment crypto cryptocurrency'.split())


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--subreddits', default=os.getenv('SUBREDDITS', DEFAULT_SUBREDDITS))
    parser.add_argument('--limit', type=int, default=10, help='Recent posts per subreddit (1-25)')
    parser.add_argument('--comments-per-post', type=int, default=10, help='Top-level comments per post (0-20)')
    args = parser.parse_args()
    if not 1 <= args.limit <= 25 or not 0 <= args.comments_per_post <= 20:
        parser.error('limit must be 1-25; comments-per-post must be 0-20')
    required = ('REDDIT_CLIENT_ID', 'REDDIT_CLIENT_SECRET', 'REDDIT_USERNAME', 'REDDIT_PASSWORD', 'REDDIT_USER_AGENT')
    missing = [name for name in required if not os.getenv(name)]
    if missing:
        parser.error('Missing environment variables: ' + ', '.join(missing))
    reddit = praw.Reddit(client_id=os.environ['REDDIT_CLIENT_ID'], client_secret=os.environ['REDDIT_CLIENT_SECRET'], username=os.environ['REDDIT_USERNAME'], password=os.environ['REDDIT_PASSWORD'], user_agent=os.environ['REDDIT_USER_AGENT'], ratelimit_seconds=60)
    output = Path('reports')
    output.mkdir(exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
    rows = []
    tokens = Counter()
    for name in [s.strip().removeprefix('r/') for s in args.subreddits.split(',') if s.strip()]:
        if not re.fullmatch(r'[A-Za-z0-9_]{2,21}', name):
            parser.error(f'Invalid subreddit: {name}')
        for submission in reddit.subreddit(name).new(limit=args.limit):
            title = submission.title
            tokens.update(w for w in re.findall(r"[a-z]{4,}", title.lower()) if w not in STOPWORDS)
            rows.append({'subreddit': name, 'type': 'post', 'created_utc': datetime.fromtimestamp(submission.created_utc, timezone.utc).isoformat(), 'score': submission.score, 'comment_count': submission.num_comments, 'title': title})
            if args.comments_per_post:
                submission.comment_sort = 'top'
                submission.comments.replace_more(limit=0)
                for comment in submission.comments[:args.comments_per_post]:
                    # No usernames, comment bodies, or user identifiers are retained.
                    rows.append({'subreddit': name, 'type': 'comment', 'created_utc': datetime.fromtimestamp(comment.created_utc, timezone.utc).isoformat(), 'score': comment.score, 'comment_count': '', 'title': ''})
    path = output / f'aggregate_{timestamp}.csv'
    with path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['subreddit', 'type', 'created_utc', 'score', 'comment_count', 'title'])
        writer.writeheader()
        writer.writerows(rows)
    trend_path = output / f'top_title_terms_{timestamp}.csv'
    with trend_path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['term', 'frequency'])
        writer.writerows(tokens.most_common(30))
    print(f'Saved {len(rows)} records to {path} and top title terms to {trend_path}')
    print('Delete reports when no longer needed; reports are not automatically synchronized with Reddit deletions.')


if __name__ == '__main__':
    main()
