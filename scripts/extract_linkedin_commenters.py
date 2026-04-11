"""Fetch a LinkedIn post's comments and extract each commenter's LinkedIn URL."""
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


def fetch_post(client, activity_id):
    """Fetch the LinkedIn post for context."""
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
            print(f"Error fetching post: {e}")

    if isinstance(post, dict) and "post" in post:
        post = post["post"]

    return post


def fetch_comments(client, activity_id):
    """Fetch comments on the LinkedIn post."""
    try:
        result = client.execute_tool("get_linkedin_post_comments", {
            "activityId": activity_id,
        })
        if isinstance(result, dict):
            comments = result.get("comments", result.get("data", []))
        elif isinstance(result, list):
            comments = result
        else:
            comments = []
        return comments
    except Exception as e:
        print(f"Error fetching comments: {e}")
        return []


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_linkedin_commenters.py <linkedin_post_url>")
        sys.exit(1)

    url = sys.argv[1]
    original_url = sys.argv[2] if len(sys.argv) > 2 else url
    activity_id = extract_activity_id(url)

    if not activity_id:
        print(f"Error: Could not extract activity ID from URL: {url}")
        print("If this is an iOS share link, resolve it first via the DataGen custom tool")
        print("  resolve_linkedin_activity_id (UUID: 1686275b-8309-43b6-95fb-49d2c9dfedd0)")
        sys.exit(1)

    client = DatagenClient()

    # Step 1: Fetch the post for context
    print(f"Fetching post: {activity_id}")
    post = fetch_post(client, activity_id)

    post_author = "Unknown"
    post_text = ""
    post_reactions = 0
    post_comments_count = 0
    if post:
        author = post.get("author", {})
        post_author = author.get("authorName", "Unknown")
        post_text = post.get("text", "")
        post_reactions = post.get("reactionsCount", 0)
        post_comments_count = post.get("commentsCount", 0)

    # Step 2: Fetch comments
    print(f"Fetching comments...")
    comments = fetch_comments(client, activity_id)
    print(f"Found {len(comments)} comments")

    # Step 3: Extract commenters and their LinkedIn URLs (no profile fetching)
    commenters = []
    seen_urls = set()

    for comment in comments:
        commenter = comment.get("author", comment.get("commenter", {}))
        if isinstance(commenter, str):
            commenters.append({
                "name": commenter,
                "headline": "",
                "url": "",
                "comment_text": comment.get("text", comment.get("comment", "")),
            })
            continue

        commenter_name = commenter.get("authorName", commenter.get("name", "Unknown"))
        commenter_url = commenter.get("authorUrl", commenter.get("url", commenter.get("linkedInUrl", "")))
        commenter_headline = commenter.get("authorHeadline", commenter.get("headline", ""))
        comment_text = comment.get("text", comment.get("comment", ""))

        is_new = commenter_url and commenter_url not in seen_urls
        if commenter_url:
            seen_urls.add(commenter_url)

        commenters.append({
            "name": commenter_name,
            "headline": commenter_headline,
            "url": commenter_url,
            "comment_text": comment_text,
            "is_unique": is_new,
        })

    unique_count = sum(1 for c in commenters if c.get("is_unique"))

    # Step 4: Build output markdown
    today = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(f"{post_author} commenters")
    filename = f"{today}-linkedin-commenters-{slug}.md"

    sections = []
    sections.append(f"""---
title: "LinkedIn commenters on post by {post_author}"
source: "{url}"
original_link: "{original_url}"
saved: {today}
type: linkedin-commenters
post_author: "{post_author}"
activity_id: "{activity_id}"
total_comments: {len(comments)}
unique_commenters: {unique_count}
post_reactions: {post_reactions}
post_comments: {post_comments_count}
tags: []
---

# Commenters on post by {post_author}

**Post excerpt:** {post_text[:200]}{"..." if len(post_text) > 200 else ""}
**Engagement:** {post_reactions} reactions, {post_comments_count} comments
**Unique commenters:** {unique_count}

---
""")

    # Section: Commenters list
    sections.append("## Commenters\n")

    for c in commenters:
        name = c.get("name", "Unknown")
        headline = c.get("headline", "")
        commenter_url = c.get("url", "")

        if commenter_url:
            sections.append(f"### [{name}]({commenter_url})")
        else:
            sections.append(f"### {name}")
        if headline:
            sections.append(f"**{headline}**")

        comment_text = c.get("comment_text", "")
        if comment_text:
            short_comment = comment_text[:200] + ("..." if len(comment_text) > 200 else "")
            sections.append(f'\n**Comment:** "{short_comment}"')

        sections.append("")  # blank line between commenters

    # Summary table
    sections.append("---\n## Summary Table\n")
    sections.append("| Name | Headline | LinkedIn |")
    sections.append("|---|---|---|")
    seen_in_table = set()
    for c in commenters:
        commenter_url = c.get("url", "")
        if commenter_url in seen_in_table:
            continue
        if commenter_url:
            seen_in_table.add(commenter_url)
        name = c.get("name", "Unknown")
        headline = (c.get("headline", "") or "").replace("|", "/")
        link = f"[Profile]({commenter_url})" if commenter_url else "N/A"
        sections.append(f"| {name} | {headline} | {link} |")

    content = "\n".join(sections) + "\n"

    # Save under raw/{date}/
    date_dir = os.path.join("raw", today)
    os.makedirs(date_dir, exist_ok=True)
    filepath = os.path.join(date_dir, filename)
    with open(filepath, "w") as f:
        f.write(content)

    print(f"\nSaved: {filepath}")
    print(f"Post by: {post_author}")
    print(f"Comments: {len(comments)}")
    print(f"Unique commenters: {unique_count}")


if __name__ == "__main__":
    main()
