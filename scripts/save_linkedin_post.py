"""Fetch a LinkedIn post via DataGen and save to raw/ as markdown."""
import os
import sys
import re
import json
from datetime import datetime
from datagen_sdk import DatagenClient


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text[:80].strip('-')


def extract_activity_id(url):
    """Extract activity ID from a canonical LinkedIn post URL."""
    url = url.strip()

    # Format 1: /feed/update/urn:li:activity:XXXXX
    m = re.search(r'urn:li:activity:(\d+)', url)
    if m:
        return m.group(1)

    # Format 2: /posts/username_slug-activity-XXXXX-hash
    m = re.search(r'-activity-(\d{15,20})-', url)
    if m:
        return m.group(1)

    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python save_linkedin_post.py <linkedin_post_url>")
        sys.exit(1)

    url = sys.argv[1]
    activity_id = extract_activity_id(url)

    if not activity_id:
        print(f"Error: Could not extract activity ID from URL: {url}")
        print("If this is an iOS share link, resolve it first via the DataGen custom tool")
        print("  resolve_linkedin_activity_id (UUID: 1686275b-8309-43b6-95fb-49d2c9dfedd0)")
        sys.exit(1)

    canonical_url = url

    client = DatagenClient()
    print(f"Fetching LinkedIn post: {activity_id}")

    # Try person post first, fall back to company post
    post = None
    try:
        result = client.execute_tool("get_linkedin_person_post", {
            "activityId": activity_id,
        })
        post = result.get("post") if isinstance(result, dict) else result
    except Exception as e:
        print(f"Person post lookup failed, trying company post: {e}")

    if not post:
        try:
            result = client.execute_tool("get_linkedin_company_post", {
                "activity_id": activity_id,
            })
            post = result.get("post") if isinstance(result, dict) else result
        except Exception as e:
            print(f"Error: Could not fetch post: {e}")
            sys.exit(1)

    if not post:
        print("Error: No post data returned")
        sys.exit(1)

    # Handle nested response formats
    if isinstance(post, dict) and "post" in post:
        post = post["post"]

    text = post.get("text", "")
    author = post.get("author", {})
    author_name = author.get("authorName", "Unknown")
    author_headline = author.get("authorHeadline", "")
    author_url = author.get("authorUrl", "")
    activity_date = post.get("activityDate", "")
    reactions = post.get("reactionsCount", 0)
    comments = post.get("commentsCount", 0)
    share_url = post.get("shareUrl", "") or post.get("activityUrl", "") or canonical_url or url

    # Related/reposted content
    related = post.get("relatedPost")
    related_section = ""
    if related and related.get("text"):
        related_author = related.get("author", {})
        related_section = f"""

---

**Repost of [{related_author.get('authorName', 'Unknown')}]({related_author.get('authorUrl', '')})**

{related.get('text', '')}
"""

    if not text and not related_section:
        print("Error: Post has no text content")
        sys.exit(1)

    # Generate filename
    today = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(f"{author_name} {text[:50]}")
    filename = f"{today}-linkedin-{slug}.md"

    word_count = len(text.split())
    content = f"""---
title: "LinkedIn post by {author_name}"
source: "{share_url}"
saved: {today}
type: linkedin-post
author: "{author_name}"
author_headline: "{author_headline}"
author_url: "{author_url}"
activity_id: "{activity_id}"
activity_date: "{activity_date}"
reactions: {reactions}
comments: {comments}
words: {word_count}
tags: []
---

{text}{related_section}
"""

    # Save under raw/{date}/
    date_dir = os.path.join("raw", today)
    os.makedirs(date_dir, exist_ok=True)
    filepath = os.path.join(date_dir, filename)
    with open(filepath, "w") as f:
        f.write(content)

    print(f"Saved: {filepath} ({word_count} words)")
    print(f"Author: {author_name}")
    print(f"Engagement: {reactions} reactions, {comments} comments")


if __name__ == "__main__":
    main()
