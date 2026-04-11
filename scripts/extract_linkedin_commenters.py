"""Fetch a LinkedIn post's comments and pull each commenter's LinkedIn profile."""
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
        # Handle various response shapes
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


def fetch_commenter_profile(client, linkedin_url):
    """Fetch a commenter's full LinkedIn profile."""
    try:
        result = client.execute_tool("get_linkedin_person_data", {
            "linkedin_url": linkedin_url,
        })
        if isinstance(result, dict):
            return result.get("person", result.get("data", result))
        return result
    except Exception as e:
        print(f"  Could not fetch profile for {linkedin_url}: {e}")
        return None


def format_profile(profile):
    """Format a LinkedIn profile into readable markdown."""
    if not profile:
        return ""

    name = profile.get("fullName", profile.get("name", "Unknown"))
    headline = profile.get("headline", "")
    location = profile.get("location", "")
    summary = profile.get("summary", "")
    url = profile.get("linkedInUrl", profile.get("url", profile.get("linkedin_url", "")))
    company = profile.get("company", profile.get("currentCompany", ""))
    title = profile.get("title", profile.get("currentTitle", profile.get("position", "")))
    followers = profile.get("followersCount", profile.get("followers", ""))

    lines = []
    lines.append(f"### [{name}]({url})")
    if headline:
        lines.append(f"**{headline}**")
    parts = []
    if title and company:
        parts.append(f"{title} at {company}")
    elif title:
        parts.append(title)
    elif company:
        parts.append(company)
    if location:
        parts.append(location)
    if followers:
        parts.append(f"{followers} followers")
    if parts:
        lines.append(" | ".join(parts))
    if summary:
        # Truncate long summaries
        short = summary[:300].rsplit(" ", 1)[0] + ("..." if len(summary) > 300 else "")
        lines.append(f"\n> {short}")

    return "\n".join(lines)


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

    # Step 3: Extract unique commenters and fetch their profiles
    commenters = []
    seen_urls = set()

    for comment in comments:
        commenter = comment.get("author", comment.get("commenter", {}))
        if isinstance(commenter, str):
            # Sometimes just a name string
            commenters.append({
                "name": commenter,
                "comment_text": comment.get("text", comment.get("comment", "")),
                "profile": None,
            })
            continue

        commenter_name = commenter.get("authorName", commenter.get("name", "Unknown"))
        commenter_url = commenter.get("authorUrl", commenter.get("url", commenter.get("linkedInUrl", "")))
        commenter_headline = commenter.get("authorHeadline", commenter.get("headline", ""))
        comment_text = comment.get("text", comment.get("comment", ""))

        # Deduplicate by LinkedIn URL
        profile = None
        if commenter_url and commenter_url not in seen_urls:
            seen_urls.add(commenter_url)
            print(f"  Fetching profile: {commenter_name} ({commenter_url})")
            profile = fetch_commenter_profile(client, commenter_url)

        commenters.append({
            "name": commenter_name,
            "headline": commenter_headline,
            "url": commenter_url,
            "comment_text": comment_text,
            "profile": profile,
        })

    # Step 4: Build output markdown
    today = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(f"{post_author} commenters")
    filename = f"{today}-linkedin-commenters-{slug}.md"

    unique_profiles = [c for c in commenters if c.get("profile")]

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
unique_profiles_fetched: {len(unique_profiles)}
post_reactions: {post_reactions}
post_comments: {post_comments_count}
tags: []
---

# Commenters on post by {post_author}

**Post excerpt:** {post_text[:200]}{"..." if len(post_text) > 200 else ""}
**Engagement:** {post_reactions} reactions, {post_comments_count} comments
**Profiles fetched:** {len(unique_profiles)} / {len(comments)} commenters

---
""")

    # Section: Commenter profiles
    sections.append("## Commenter Profiles\n")

    for i, c in enumerate(commenters, 1):
        profile_md = format_profile(c.get("profile"))
        if profile_md:
            sections.append(profile_md)
        else:
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
    sections.append("| Name | Headline | Profile |")
    sections.append("|---|---|---|")
    for c in commenters:
        name = c.get("name", "Unknown")
        headline = c.get("headline", "")
        if not headline and c.get("profile"):
            headline = c["profile"].get("headline", "")
        commenter_url = c.get("url", "")
        link = f"[Profile]({commenter_url})" if commenter_url else "N/A"
        # Escape pipes in headline
        headline = headline.replace("|", "/")
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
    print(f"Profiles fetched: {len(unique_profiles)}")


if __name__ == "__main__":
    main()
