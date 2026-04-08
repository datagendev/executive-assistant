---
name: executive-assistant
description: Check calendar availability and share free time slots. Use when someone asks "what's my availability?", "when am I free?", or "find me a time".
---

# Availability Checker

Show your available time slots from Google Calendar so you can share them with others.

## Usage

Called by the executive-assistant agent, or directly:
```bash
/executive-assistant              # Show availability for rest of today
/executive-assistant tomorrow     # Show availability for tomorrow
/executive-assistant this week    # Show availability for the rest of this week
/executive-assistant 2026-04-10   # Show availability for a specific date
```

## Workflow

### Step 1: Get current time and determine date range

Call `composio_GOOGLECALENDAR_GET_CURRENT_DATE_TIME` via DataGen `executeTool` to get the current timestamp.

Parse the user's request to determine the date range:
- No argument or "today": from now until end of today
- "tomorrow": full next day
- "this week": from now until end of Friday
- Specific date: full day for that date

The user's timezone is **America/Chicago** (CDT, UTC-5). Always use this timezone offset when constructing timeMin/timeMax to avoid the UTC mismatch problem.

### Step 2: Fetch events and free slots in parallel

Make two parallel DataGen `executeTool` calls:

**Call 1: Get events for context**
```
Tool: composio_GOOGLECALENDAR_EVENTS_LIST
Params:
  timeMin: "<start>T00:00:00-05:00"  (use -05:00 for CDT)
  timeMax: "<end>T23:59:59-05:00"
  singleEvents: true
  orderBy: "startTime"
```

**Call 2: Get free slots**
```
Tool: composio_GOOGLECALENDAR_FIND_FREE_SLOTS
Params:
  time_min: "<start>T00:00:00-05:00"
  time_max: "<end>T23:59:59-05:00"
  timezone: "America/Chicago"
```

### Step 3: Format output

Present a clean, copy-pasteable availability summary. Two sections:

**Section 1: Schedule overview** (what's booked)
List each event with time and title. Keep it brief.

**Section 2: Available slots**
List free time windows, filtered to reasonable working hours (9 AM - 6 PM CDT unless user specifies otherwise). Format as:

```
## Available times - Tuesday, April 8

- 10:30 AM - 1:00 PM CDT (2.5 hrs)
- 1:30 PM - 3:30 PM CDT (2 hrs)
- 4:30 PM - 6:00 PM CDT (1.5 hrs)
```

This format is designed to be copy-pasted directly into a message, email, or Slack.

### Step 4: Offer next actions

After showing availability, ask:
- "Want me to share these slots in an email or message?"
- "Want me to book a specific slot?"

## Rules

- Always use America/Chicago timezone with explicit offset (never UTC "Z" suffix)
- Filter free slots to working hours (9 AM - 6 PM) by default
- If showing multiple days, group by date
- Keep event titles visible (the user needs context on what's blocking time)
- Do not show declined events as busy
- Round slot boundaries to nearest 15 minutes for cleaner output
