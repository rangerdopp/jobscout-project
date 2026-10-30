import json
import os
from datetime import datetime, timezone
from email.utils import format_datetime
from xml.sax.saxutils import escape

owner = os.environ.get("GITHUB_REPOSITORY_OWNER", "YOURUSERNAME")
repo = os.environ.get("GITHUB_REPOSITORY", f"{owner}/jobscout-project").split("/")[-1]
SITE = f"https://{owner}.github.io/{repo}/"

with open("public/data/jobs.json", encoding="utf-8") as f:
    data = json.load(f)

jobs = data["jobs"] if isinstance(data, dict) else data

items = []
for j in jobs[:100]:
    url = j.get("url") or j.get("link")
    if not url:
        continue
    title = j.get("title", "Untitled")
    company = j.get("company", "")
    location = j.get("location", "")
    items.append(
        "<item>"
        f"<title>{escape(title)}{' at ' + escape(company) if company else ''}</title>"
        f"<link>{escape(url)}</link>"
        f'<guid isPermaLink="false">{escape(url)}</guid>'
        f"<description>{escape(location)}</description>"
        "</item>"
    )

feed = (
    '<?xml version="1.0" encoding="UTF-8"?>'
    '<rss version="2.0"><channel>'
    "<title>JobScout</title>"
    f"<link>{SITE}</link>"
    "<description>Daily job leads</description>"
    f"<lastBuildDate>{format_datetime(datetime.now(timezone.utc))}</lastBuildDate>"
    + "".join(items)
    + "</channel></rss>"
)

with open("public/feed.xml", "w", encoding="utf-8") as f:
    f.write(feed)

print(f"Wrote feed with {len(items)} items")
