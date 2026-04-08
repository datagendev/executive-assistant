---
name: ea-book
description: Book a meeting on Google Calendar. Use when user says "book a meeting", "schedule a call", "set up time with", or "create an event".
---

# Book Meeting

Create a calendar event with optional attendees, free slot checking, and invite sending.

## Workflow

### Step 1: Parse the request

Extract from user input:
- **What**: meeting title/purpose
- **Who**: attendee emails (if mentioned)
- **When**: specific time, or "find a time" 
- **How long**: duration (default 30 min)

If any required info is missing, ask the user.

### Step 2: Check availability (if time not specified)

If user says "find a time" or gives a date range:
1. Call `composio_GOOGLECALENDAR_FIND_FREE_SLOTS` via DataGen `executeTool` for the date range
2. Present 3-5 available slots
3. Let user pick one

If attendee emails are provided, check their free/busy too using `composio_GOOGLECALENDAR_FREE_BUSY_QUERY`.

### Step 3: Create the event

Call `composio_GOOGLECALENDAR_CREATE_EVENT` via DataGen `executeTool`:
```
Params:
  summary: "<meeting title>"
  start_datetime: "YYYY-MM-DDTHH:MM:SS"
  timezone: "America/Chicago"
  event_duration_hour: <hours>
  event_duration_minutes: <minutes>
  attendees: ["email1@example.com", "email2@example.com"]
  description: "<any context from the user>"
```

### Step 4: Confirm

Show the user:
- Event title
- Date/time in CDT
- Attendees (if any)
- Google Calendar link

## Rules

- Always use timezone "America/Chicago"
- Default duration is 30 minutes unless specified
- Always confirm before creating the event
- Include Google Meet link by default (the tool adds it automatically)
