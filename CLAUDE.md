# Executive Assistant for Claude Code

This project is a personal executive assistant built as a Claude Code agent with modular skills. It uses Google Calendar and Gmail via DataGen's Composio integration, and manages a local todo list.

## Prerequisites

- [Claude Code](https://claude.ai/code) installed
- [DataGen](https://datagen.dev) account with MCP configured (`/datagen:setup`)
- Composio Google Calendar connected in DataGen
- Composio Gmail connected in DataGen

## Quick Start

```bash
# Clone and enter the repo
git clone https://github.com/datagendev/executive-assistant.git
cd executive-assistant

# Set up DataGen if not already configured
/datagen:setup
```

## Usage

The executive-assistant agent routes to the right skill automatically:

| Command | What it does |
|---|---|
| `/ea-briefing` | Morning briefing: schedule + todos + emails + meeting prep |
| `/executive-assistant` | Show calendar availability / free slots |
| `/ea-book` | Book a meeting on Google Calendar |
| `/ea-todo` | Add, triage, complete, or review tasks in todo.md |

Or just talk naturally and the agent figures it out:
- "What's my availability tomorrow?"
- "Book a 30 min call with john@acme.com"
- "I need to fix the API bug and prep the deck"
- "Briefing"

## Architecture

```
.claude/
  agents/
    executive-assistant.md    # Agent definition, routes to skills
  skills/
    executive-assistant/      # Calendar availability checker
    ea-book/                  # Meeting booking
    ea-todo/                  # Local todo.md manager
    ea-briefing/              # Morning briefing with meeting prep
  context/
    ea-preferences.md         # User preferences, blocklists, triage rules
todo.md                       # Local task tracker (Now/Next/Later/Done)
```

## Customization

Edit `.claude/context/ea-preferences.md` to configure:
- Email blocklist (senders to skip in briefings)
- Email triage rules (what counts as urgent vs FYI)
- Todo format preferences
- Calendar timezone and working hours

## DataGen Tools Used

| Function | Tool |
|---|---|
| Current time | `composio_GOOGLECALENDAR_GET_CURRENT_DATE_TIME` |
| List events | `composio_GOOGLECALENDAR_EVENTS_LIST` |
| Free slots | `composio_GOOGLECALENDAR_FIND_FREE_SLOTS` |
| Create event | `composio_GOOGLECALENDAR_CREATE_EVENT` |
| Free/busy query | `composio_GOOGLECALENDAR_FREE_BUSY_QUERY` |
| Fetch emails | `composio_GMAIL_FETCH_EMAILS` |
| LinkedIn search | `search_linkedin_person` |
| LinkedIn profile | `get_linkedin_person_data` |
