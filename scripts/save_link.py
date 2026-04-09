"""Fetch an article via Firecrawl and save to raw/ as markdown."""
import os
import sys
import json
import re
from datetime import datetime
from datagen_sdk import DatagenClient

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text[:80].strip('-')

def main():
    if len(sys.argv) < 2:
        print("Usage: python save_link.py <url>")
        sys.exit(1)

    url = sys.argv[1]
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
