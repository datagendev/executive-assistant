---
name: ea-save-link
description: Save an article, blog post, YouTube transcript, or LinkedIn post by fetching its content and storing it locally in raw/. Use when user says "save this article", "read later", "fetch this post", or pastes an article/YouTube/LinkedIn URL to save.
---

# Save Link

Fetch an article, blog post, documentation page, YouTube transcript, or LinkedIn post, extract the content as markdown, and save it to the `raw/` folder for later reading. YouTube and LinkedIn links are automatically detected and routed to their respective fetchers.

## Workflow

### Step 1: Parse the URL

Extract the URL from the user's message. If multiple URLs, process each one.

### Step 2: Run the save script

Use the SDK script to fetch and save in one step (avoids dumping large content into context):

```bash
source .venv/bin/activate && set -a && source .env && set +a && python scripts/save_link.py "<url>"
```

This script:
- Detects YouTube links and routes to `scripts/save_youtube.py` (Supadata API)
- Detects LinkedIn post links and routes to `scripts/save_linkedin_post.py` (DataGen LinkedIn tools)
- For articles: fetches via Firecrawl (`mcp_Firecrawl_firecrawl_scrape`) using the DataGen SDK
- Extracts main content as markdown
- Generates a dated, slugified filename
- Saves to `raw/` with frontmatter (title, source, date, word count, tags)

### Step 3: Confirm

The script prints the saved filename and word count. Tell the user:
- File saved to `raw/<filename>.md`
- Title and word count
- Suggest: "Want me to add a reading task to your todo?"

## YouTube Support

YouTube links (`youtube.com/watch`, `youtu.be/`, `youtube.com/shorts/`) are automatically detected and routed to `scripts/save_youtube.py`, which:
- Fetches the transcript via Supadata API (key loaded from `.env` as `SUPADATA_API_KEY`)
- Saves as markdown with `type: youtube-transcript` in frontmatter
- Includes language detection

## LinkedIn Post Support

LinkedIn post links (`linkedin.com/feed/update/`, `linkedin.com/posts/`) are automatically detected and routed to `scripts/save_linkedin_post.py`, which:
- Extracts the activity ID from the URL
- Fetches post via `get_linkedin_person_post` (falls back to `get_linkedin_company_post`)
- Saves as markdown with `type: linkedin-post` in frontmatter
- Includes author info, engagement metrics, and reposted content if present

### iOS Share Links

iOS share links contain `-share-` instead of `-activity-` in the URL, so the activity ID cannot be extracted directly. When you detect an iOS share link (contains `-share-` or `utm_medium=ios_app`):

1. First, run the DataGen custom tool `resolve_linkedin_activity_id` (UUID: `1686275b-8309-43b6-95fb-49d2c9dfedd0`) via `submitCustomToolRun` with `{"post_url": "<ios_url>"}` to get the canonical URL
2. Then pass the returned `canonical_url` to the save script:
   ```bash
   source .venv/bin/activate && set -a && source .env && set +a && python scripts/save_linkedin_post.py "<canonical_url>"
   ```

## Original Link Preservation

Always save the original link the user pasted alongside any resolved/canonical URL. Each script accepts an optional second argument for the original URL:

```bash
python scripts/save_link.py "<resolved_url>" "<original_url>"
python scripts/save_youtube.py "<url>" "<lang>"
python scripts/save_linkedin_post.py "<canonical_url>" "<original_url>"
```

Example test links for each type:
- **Article**: `https://example.com/blog/some-article`
- **YouTube**: `https://www.youtube.com/watch?v=knx2wrILP1M`
- **LinkedIn (canonical)**: `https://www.linkedin.com/posts/jacob-dietle_8296-articles-tweets-newsletters-and-activity-7448034500640575488-rI7q`
- **LinkedIn (iOS share)**: `https://www.linkedin.com/posts/jacob-dietle_8296-articles-tweets-newsletters-and-share-7448034499063484416-DIaZ?utm_source=social_share_send&utm_medium=ios_app`

## Rules

- Always use the script, not the MCP tool directly (saves tokens)
- If the script fails, check the URL is valid and accessible
- If the URL is behind a paywall, tell the user
- Tags field is empty by default; user can add later
