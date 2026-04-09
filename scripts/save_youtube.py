"""Fetch a YouTube transcript via Supadata API and save to raw/ as markdown."""
import os
import sys
import re
import requests
from datetime import datetime


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text[:80].strip('-')


def main():
    if len(sys.argv) < 2:
        print("Usage: python save_youtube.py <youtube_url>")
        sys.exit(1)

    url = sys.argv[1]
    lang = sys.argv[2] if len(sys.argv) > 2 else "en"

    api_key = os.environ.get("SUPADATA_API_KEY")
    if not api_key:
        print("Error: SUPADATA_API_KEY env var not set")
        sys.exit(1)

    print(f"Fetching transcript: {url}")
    resp = requests.get(
        "https://api.supadata.ai/v1/youtube/transcript",
        params={"url": url, "text": "true", "lang": lang},
        headers={"x-api-key": api_key},
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()

    transcript = data.get("content", "")
    transcript_lang = data.get("lang", "unknown")

    if not transcript:
        print("Error: No transcript returned")
        sys.exit(1)

    # Extract video ID for title fallback
    video_id = re.search(r'(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})', url)
    video_id = video_id.group(1) if video_id else "unknown"

    # Try to get video title from page
    title = f"YouTube {video_id}"
    try:
        page = requests.get(url, timeout=10)
        match = re.search(r'<title>(.*?)</title>', page.text)
        if match:
            title = match.group(1).replace(" - YouTube", "").strip()
    except Exception:
        pass

    # Generate filename
    today = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(title)
    filename = f"{today}-{slug}.md"

    # Build file with frontmatter
    word_count = len(transcript.split())
    content = f"""---
title: "{title}"
source: "{url}"
saved: {today}
type: youtube-transcript
language: {transcript_lang}
words: {word_count}
tags: []
---

{transcript}
"""

    # Save under raw/{date}/
    date_dir = os.path.join("raw", today)
    os.makedirs(date_dir, exist_ok=True)
    filepath = os.path.join(date_dir, filename)
    with open(filepath, "w") as f:
        f.write(content)

    print(f"Saved: {filepath} ({word_count} words)")
    print(f"Title: {title}")


if __name__ == "__main__":
    main()
