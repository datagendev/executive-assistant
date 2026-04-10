---
name: ea-prep-prospect
description: Prep for a prospect meeting by gathering email history, meeting transcripts, HeyReach messages, and LinkedIn profile/posts. Use when user says "prep for meeting with", "research prospect", "meeting prep", or names a person they're about to meet.
---

# Prep Prospect Meeting

Research a prospect before a meeting by gathering all prior touchpoints and their public profile. Data is saved to `tmp/` files first to save tokens, then compiled into a final brief.

## Workflow

This skill runs step-by-step using tasks. Each step saves raw data to `tmp/<prospect_slug>/` before the final compilation.

### Step 0: Identify the prospect

Extract the prospect's name and email from the user's message. If you don't have their LinkedIn URL, ask the user. If the user doesn't know, try to find it via:
1. Check HeyReach conversations for their profile URL
2. Use `search_linkedin_person` with their name + company
3. Use WebSearch as a last resort

### Step 1: Gmail history

Use `mcp_Gmail_Yusheng_gmail_search_emails` via DataGen `executeTool`:
```
tool: mcp_Gmail_Yusheng_gmail_search_emails
params: { "query": "from:<email> OR to:<email>", "maxResults": 20 }
```
Save results to `tmp/<slug>/01-gmail.json`.

### Step 2: Fireflies meeting transcripts

Use `mcp_Fireflies_fireflies_get_transcripts` via DataGen `executeTool`:
```
tool: mcp_Fireflies_fireflies_get_transcripts
params: { "participants": ["<email>"], "limit": 10, "format": "json" }
```
If matches found, fetch full transcripts with `mcp_Fireflies_fireflies_get_transcript` for each meeting ID.
Save results to `tmp/<slug>/02-fireflies.json`.

### Step 3: HeyReach conversation history

Use `mcp_Heyreach_get_conversations_v2` via DataGen `executeTool`:
```
tool: mcp_Heyreach_get_conversations_v2
params: { "searchString": "<prospect_name>", "linkedInAccountIds": [], "campaignIds": [], "limit": 20 }
```
If a conversation is found, fetch messages with `mcp_Heyreach_get_chatroom`.
Save results to `tmp/<slug>/03-heyreach.json`.

### Step 4: LinkedIn profile + recent posts

Use DataGen `executeTool` for both:
```
tool: get_linkedin_person_data
params: { "linkedin_url": "<linkedin_url>" }

tool: get_linkedin_person_posts
params: { "linkedin_url": "<linkedin_url>" }
```
Save profile to `tmp/<slug>/04-linkedin-profile.json`.
Save posts to `tmp/<slug>/05-linkedin-posts.json`.

### Step 5: Compile the brief

Read all files from `tmp/<slug>/`. Compile into a formatted markdown brief saved to `tmp/<slug>/brief.md` with these sections:

```markdown
# Meeting Prep: <Name>

## 1. Background
- Current role, company, headline
- Career history highlights
- Education, skills
- Recent LinkedIn activity and what topics they care about (from posts)

## 2. Prior Interactions
- **Email**: Summary of email threads, key topics discussed, last contact date
- **Meetings**: Summary of Fireflies transcripts, key decisions/action items
- **HeyReach**: LinkedIn outreach history, message exchange summary

## 3. How DataGen Can Help
Based on their role, company, pain points from conversations, and LinkedIn activity:
- Specific DataGen capabilities that map to their needs
- Talking points tied to their context
- Potential objections and responses

## 4. Suggested Agenda
- Opening (reference prior interaction or recent post)
- Discovery questions based on what we know
- Demo focus areas
- Next steps to propose
```

### Step 6: Present to user

Print the brief to the user. Offer to:
- Add meeting prep tasks to todo
- Save the brief to `raw/` for permanent storage

## Tool Reference

| Function | Tool Name | Server |
|---|---|---|
| Search emails | `mcp_Gmail_Yusheng_gmail_search_emails` | Gmail_Yusheng |
| Search transcripts | `mcp_Fireflies_fireflies_get_transcripts` | Fireflies |
| Get transcript | `mcp_Fireflies_fireflies_get_transcript` | Fireflies |
| Get summary | `mcp_Fireflies_fireflies_get_summary` | Fireflies |
| Search conversations | `mcp_Heyreach_get_conversations_v2` | Heyreach |
| Get chatroom | `mcp_Heyreach_get_chatroom` | Heyreach |
| LinkedIn profile | `get_linkedin_person_data` | (default) |
| LinkedIn posts | `get_linkedin_person_posts` | (default) |
| Search person | `search_linkedin_person` | (default) |

## Rules

- Save each step's raw data to `tmp/<slug>/` as JSON before processing
- Use tasks to track progress through each step
- If a data source returns nothing, note "No data found" and move on
- Do not skip steps -- even empty results are useful context
- Ask the user for LinkedIn URL if not discoverable
- The "How DataGen Can Help" section must reference specific findings from steps 1-4
- Be concise in the brief, no fluff
- Clean up `tmp/<slug>/` only if user asks
