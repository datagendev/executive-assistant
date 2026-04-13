---
name: ea-extract-commenters
description: Extract commenters from a LinkedIn post and get their LinkedIn URLs. Use when user says "get commenters", "who commented on this post", "extract commenters", or pastes a LinkedIn post URL and wants commenter data.
---

# Extract LinkedIn Post Commenters

Fetch all comments on a LinkedIn post and extract each commenter's name, headline, and LinkedIn URL. Saves a structured report to `raw/`.

## Setup

Before running the script, ensure the DataGen SDK is installed in the virtual environment:

```bash
python -m venv .venv 2>/dev/null; source .venv/bin/activate && pip install datagen-sdk
```

This only needs to run once per environment. The SDK provides `DatagenClient` used by the extraction script.

## Workflow

### Step 1: Parse the URL

Extract the LinkedIn post URL from the user's message. Must be a `linkedin.com/posts/` or `linkedin.com/feed/update/` link.

### Step 2: Handle iOS share links

If the URL contains `-share-` or `utm_medium=ios_app`, resolve it first:

1. Run the DataGen custom tool `resolve_linkedin_activity_id` (UUID: `1686275b-8309-43b6-95fb-49d2c9dfedd0`) via `submitCustomToolRun` with `{"post_url": "<ios_url>"}` to get the canonical URL
2. Use the returned `canonical_url` in the next step

### Step 3: Run the extraction script

```bash
source .venv/bin/activate && set -a && source .env && set +a && python scripts/extract_linkedin_commenters.py "<url>"
```

For iOS share links where you resolved the canonical URL:
```bash
source .venv/bin/activate && set -a && source .env && set +a && python scripts/extract_linkedin_commenters.py "<canonical_url>" "<original_url>"
```

This script:
- Extracts the activity ID from the URL
- Fetches the post via `get_linkedin_person_post` (falls back to `get_linkedin_company_post`)
- Fetches all comments via `get_linkedin_post_comments`
- Extracts each commenter's name, headline, and LinkedIn URL directly from the comment data (no extra API calls)
- Deduplicates commenters in the summary table
- Saves to `raw/{date}/{date}-linkedin-commenters-{slug}.md`

### Step 4: Confirm

The script prints the saved filename and stats. Tell the user:
- File saved to `raw/<filename>.md`
- Number of comments found and unique commenters

### Step 5: Profile enrichment (optional, OFF by default)

Enriching each commenter's full LinkedIn profile takes ~5-10 minutes for large posts (500+ comments) and uses API credits. **Do NOT run this unless the user explicitly asks** for enrichment, full profiles, titles, companies, or similar detail.

If the user requests enrichment:

```bash
python scripts/enrich_commenters.py tmp/commenter_slugs.json
```

This script:
- Reads the commenter slugs JSON from Step 3
- Fetches each profile via `get_linkedin_person_data` concurrently (rate-limited to 50 rpm)
- Checkpoints progress to `tmp/commenter_slugs_checkpoint.json` -- safe to interrupt and resume
- Writes enriched output to `tmp/commenter_slugs_enriched.json`

Tell the user before starting:
- "Enriching {N} profiles will take ~{N/60:.0f} minutes. Want me to proceed?"
- If interrupted, re-running picks up where it left off

## Fallback: If `get_linkedin_post_comments` is unavailable

If the DataGen tool `get_linkedin_post_comments` is not available or fails:

1. Fetch the post using `get_linkedin_person_post` to confirm it exists and get the comment count
2. Tell the user the comment count and that automatic comment extraction isn't available
3. Offer to research specific commenters if the user can provide their names or LinkedIn URLs

## Output Format

The saved file includes:
- **Frontmatter**: post author, activity ID, comment/reaction counts, unique commenters count
- **Commenters list**: each commenter's name (linked to LinkedIn), headline, and comment text
- **Summary table**: deduplicated table with name, headline, and LinkedIn profile link

## Tools Used

| Function | Tool Name |
|---|---|
| Fetch person post | `get_linkedin_person_post` |
| Fetch company post | `get_linkedin_company_post` |
| Fetch post comments | `get_linkedin_post_comments` |
| Resolve iOS share link | `resolve_linkedin_activity_id` (custom tool) |

## Rules

- Always use the script, not the tools directly (saves tokens and keeps context clean)
- If the script fails on the comments step, check if the tool name is correct and try the fallback workflow
- Keep comment text excerpts to 200 characters in the output
