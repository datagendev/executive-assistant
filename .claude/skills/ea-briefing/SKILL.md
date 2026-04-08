---
name: ea-briefing
description: Morning briefing that combines today's calendar, todo list, goals, emails, and meeting prep with LinkedIn background research on attendees. Use when user says "briefing", "morning brief", "prep my day", or "what's on today".
---

# Morning Briefing

Read @.claude/context/ea-preferences.md before running for blocklist, triage rules, and formatting preferences.

Compile a comprehensive daily briefing: schedule, todos, goals, email highlights, and deep meeting prep with attendee research.

## Workflow

### Step 1: Gather context (parallel)

Run these in parallel:

**1a. Current time**
```
Tool: composio_GOOGLECALENDAR_GET_CURRENT_DATE_TIME (via DataGen executeTool)
```

**1b. Today's calendar events**
```
Tool: composio_GOOGLECALENDAR_EVENTS_LIST (via DataGen executeTool)
Params:
  timeMin: "<today>T00:00:00-05:00"
  timeMax: "<today>T23:59:59-05:00"
  singleEvents: true
  orderBy: "startTime"
```

**1c. Read todo.md**
Read `./todo.md` for current tasks across Now / Next / Later sections.

**1d. Read goals and focus**
Read `./canon/positioning.md` for current company positioning and priorities. Check for any active campaigns in `./campaigns/active/`.

**1e. Recent emails (last 24 hours)**
```
Tool: composio_GMAIL_FETCH_EMAILS (via DataGen executeTool)
Params:
  user_id: "me"
  query: "newer_than:1d"
  max_results: 20
```

### Step 2: Identify meetings that need prep

From today's events, identify meetings with external attendees (anyone not @datagen.dev). These are the meetings that need background research.

For each meeting needing prep, extract:
- Meeting title and time
- Attendee emails
- Any meeting description/context

### Step 3: Research attendees (parallel per meeting)

For each external attendee, run in parallel:

**3a. LinkedIn lookup**
```
Tool: search_linkedin_person (via DataGen executeTool)
Params:
  name: "<attendee name from email>"
  company: "<extracted from email domain>"
```

If found, get full profile:
```
Tool: get_linkedin_person_data (via DataGen executeTool)
Params:
  linkedin_url: "<url from search result>"
```

**3b. Previous email exchanges**
```
Tool: composio_GMAIL_FETCH_EMAILS (via DataGen executeTool)
Params:
  user_id: "me"
  query: "from:<attendee email> OR to:<attendee email>"
  max_results: 5
```

### Step 4: Compile briefing

Format the briefing as a clean, scannable report:

```markdown
# Daily Briefing - [Day, Month Date]
Current time: [HH:MM AM/PM CDT]

## Schedule
[Time] | [Event title] | [Duration] | [Location/Link]
...

## Todos
### Now (do today)
- [ ] ...
### Next (this week)
- [ ] ...

## Email Highlights
- [urgent/action/fyi] Subject - From (time)
...
[X unread, Y requiring action]

## Meeting Prep

### [Meeting Title] - [Time]
**Attendees:**
- [Name] - [Title] at [Company]
  LinkedIn: [headline]
  Background: [1-2 sentence summary of role, company, relevant context]

**Previous exchanges:**
- [Date]: [Brief summary of last email thread]
- [Date]: [Earlier thread if exists]

**Context/Agenda:**
[From meeting description or inferred from email threads]

**Suggested talking points:**
- [Based on attendee background and previous exchanges]
- [Based on current goals and positioning]

---
[Repeat for each meeting needing prep]
```

### Step 5: Offer actions

After the briefing, suggest:
- "Want me to draft a prep email for any of these meetings?"
- "Want me to update your todo list based on today's priorities?"
- "Want me to block focus time between meetings?"

## Rules

- Always use America/Chicago timezone (CDT, UTC-5)
- Only research external attendees (skip @datagen.dev emails)
- If LinkedIn search returns no results, note it and move on, do not block the briefing
- If email search returns too much data, summarize the most recent 3 threads
- Keep attendee summaries to 1-2 sentences, focus on what's relevant to the meeting
- Never use em dashes
- Group emails by urgency: urgent (needs response today), action (needs response this week), fyi (informational)
- If no meetings need prep, skip that section entirely
- The briefing should be readable in under 2 minutes
