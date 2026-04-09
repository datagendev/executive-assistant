---
name: ea-save-link
description: Save an article, blog post, or YouTube video transcript by fetching its content and storing it locally in raw/. Use when user says "save this article", "read later", "fetch this post", or pastes an article/YouTube URL to save.
---

# Save Article

Fetch an article, blog post, documentation page, or YouTube transcript, extract the content as markdown, and save it to the `raw/` folder for later reading. YouTube links are automatically detected and routed to transcript extraction via Supadata API.

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

## Rules

- Always use the script, not the MCP tool directly (saves tokens)
- If the script fails, check the URL is valid and accessible
- If the URL is behind a paywall, tell the user
- Tags field is empty by default; user can add later
