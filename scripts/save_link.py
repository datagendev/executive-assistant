"""Fetch an article via Firecrawl and save to raw/ as markdown.
Routes YouTube links to save_youtube.py and LinkedIn posts to save_linkedin_post.py."""
import os
import sys
import json
import re
import subprocess
from datetime import datetime
from datagen_sdk import DatagenClient

YOUTUBE_PATTERNS = [
    r'(?:https?://)?(?:www\.)?youtube\.com/watch',
    r'(?:https?://)?youtu\.be/',
    r'(?:https?://)?(?:www\.)?youtube\.com/shorts/',
]

LINKEDIN_POST_PATTERNS = [
    r'(?:https?://)?(?:www\.)?linkedin\.com/feed/update/',
    r'(?:https?://)?(?:www\.)?linkedin\.com/posts/',
]

def is_youtube_url(url):
    return any(re.search(p, url) for p in YOUTUBE_PATTERNS)

def is_linkedin_post_url(url):
    return any(re.search(p, url) for p in LINKEDIN_POST_PATTERNS)

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text[:80].strip('-')

def _route_to_script(script_name, url, extra_args=None):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cmd = [sys.executable, os.path.join(script_dir, script_name), url]
    if extra_args:
        cmd.extend(extra_args)
    result = subprocess.run(cmd, capture_output=False)
    sys.exit(result.returncode)

def main():
    if len(sys.argv) < 2:
        print("Usage: python save_link.py <url> [original_url]")
        sys.exit(1)

    url = sys.argv[1]
    original_url = sys.argv[2] if len(sys.argv) > 2 else url

    # Route YouTube links to the transcript fetcher
    if is_youtube_url(url):
        _route_to_script("save_youtube.py", url)

    # Route LinkedIn post links
    if is_linkedin_post_url(url):
        _route_to_script("save_linkedin_post.py", url, [original_url])

    client = DatagenClient()

    print(f"Fetching: {url}")
    result = client.execute_tool("mcp_Firecrawl_firecrawl_scrape", {
        "url": url,
        "formats": ["markdown"],
        "onlyMainContent": True,
    })

    # Parse the response: result -> content[0] -> text (JSON string)
    content = result.get("content", [])
    if not content:
        print("Error: Empty response")
        sys.exit(1)

    data = json.loads(content[0]["text"])
    markdown = data.get("markdown", "")
    metadata = data.get("metadata", {})
    title = metadata.get("title", "Untitled")

    if not markdown:
        print("Error: No content returned")
        sys.exit(1)

    # Generate filename
    today = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(title)
    filename = f"{today}-{slug}.md"

    # Build file with frontmatter
    word_count = len(markdown.split())
    content = f"""---
title: "{title}"
source: "{url}"
original_link: "{original_url}"
saved: {today}
words: {word_count}
tags: []
---

{markdown}
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
