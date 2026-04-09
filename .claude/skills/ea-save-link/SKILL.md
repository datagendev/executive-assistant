---
name: ea-save-link
description: Save an article or blog post by fetching its content and storing it locally in raw/. Use when user says "save this article", "read later", "fetch this post", or pastes an article URL to save.
---

# Save Article

Fetch an article, blog post, or documentation page, extract the content as markdown, and save it to the `raw/` folder for later reading. Designed for online articles, not social media posts.

## Workflow

### Step 1: Parse the URL

Extract the URL from the user's message. If multiple URLs, process each one.

### Step 2: Run the save script

Use the SDK script to fetch and save in one step (avoids dumping large content into context):

```bash
python scripts/save_link.py "<url>"
```

This script:
- Fetches via Firecrawl (`mcp_Firecrawl_firecrawl_scrape`) using the DataGen SDK
- Extracts main content as markdown
- Generates a dated, slugified filename
- Saves to `raw/` with frontmatter (title, source, date, word count, tags)

Activate the venv first if needed: `source .venv/bin/activate`

### Step 3: Confirm

The script prints the saved filename and word count. Tell the user:
- File saved to `raw/<filename>.md`
- Title and word count
- Suggest: "Want me to add a reading task to your todo?"

## Rules

- Always use the script, not the MCP tool directly (saves tokens)
- If the script fails, check the URL is valid and accessible
- If the URL is behind a paywall, tell the user
- Tags field is empty by default; user can add later
