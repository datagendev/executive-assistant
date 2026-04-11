---
name: ea-extract-commenters
description: Extract commenters from a LinkedIn post and pull their LinkedIn profiles. Use when user says "get commenters", "who commented on this post", "extract commenters", or pastes a LinkedIn post URL and wants commenter data.
---

# Extract LinkedIn Post Commenters

Fetch all comments on a LinkedIn post, then pull each commenter's full LinkedIn profile. Saves a structured report with profiles and a summary table to `raw/`.

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
- For each unique commenter with a LinkedIn URL, fetches their full profile via `get_linkedin_person_data`
- Saves to `raw/{date}/{date}-linkedin-commenters-{slug}.md` with frontmatter and a summary table

### Step 4: Confirm

The script prints the saved filename and stats. Tell the user:
- File saved to `raw/<filename>.md`
- Number of comments found and profiles fetched
- Suggest: "Want me to add any of these commenters to a prospect list or research someone further?"

## Fallback: If `get_linkedin_post_comments` is unavailable

If the DataGen tool `get_linkedin_post_comments` is not available or fails, fall back to manual extraction:

1. Fetch the post using `get_linkedin_person_post` to confirm it exists and get the comment count
2. Tell the user the comment count and that automatic comment extraction isn't available
3. Offer to research specific commenters if the user can provide their names or LinkedIn URLs

## Output Format

The saved file includes:
- **Frontmatter**: post author, activity ID, comment/reaction counts, profiles fetched
- **Commenter Profiles**: each commenter's name, headline, company, location, summary, and their comment text
- **Summary Table**: quick-reference table with name, headline, and profile link

## Tools Used

| Function | Tool Name |
|---|---|
| Fetch person post | `get_linkedin_person_post` |
| Fetch company post | `get_linkedin_company_post` |
| Fetch post comments | `get_linkedin_post_comments` |
| Fetch person profile | `get_linkedin_person_data` |
| Resolve iOS share link | `resolve_linkedin_activity_id` (custom tool) |

## Rules

- Always use the script, not the tools directly (saves tokens and keeps context clean)
- If the script fails on the comments step, check if the tool name is correct and try the fallback workflow
- Deduplicate commenters by LinkedIn URL before fetching profiles
- Keep comment text excerpts to 200 characters in the output
- If a profile fetch fails for one commenter, continue with the rest
