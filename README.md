# Executive Assistant for Claude Code

A personal executive assistant built as a Claude Code agent with modular skills. Manages your calendar, email triage, todo list, and morning briefings with meeting prep.

Built with [DataGen](https://datagen.dev) for tool orchestration via Composio integrations (Google Calendar, Gmail, LinkedIn).

![Demo](demo.gif)

## What it does

- **Morning briefing** -- today's schedule, todos, email highlights, and deep meeting prep with LinkedIn background research on attendees
- **Calendar availability** -- show free time slots, copy-pasteable for sharing
- **Book meetings** -- find free slots, create events with attendees
- **Todo management** -- triage tasks into Now/Next/Later, track completion in a local `todo.md`

## Setup

### 1. Install Claude Code

If you haven't already, install [Claude Code](https://claude.ai/code).

### 2. Install the DataGen plugin

```bash
/plugin marketplace add datagendev/datagen-plugin
/plugin install datagen --scope project
```

Then **exit and restart Claude Code** for the plugin to take effect.

### 3. Set up DataGen

```
/datagen:setup
```

Follow the prompts to authenticate with your [DataGen](https://datagen.dev) account.

### 4. Connect required MCP servers

Use `/datagen:add-mcps` or add them through the UI at [datagen.dev/signalgen/mcp-servers](https://datagen.dev/signalgen/mcp-servers).

| MCP Server | Required by | What it provides |
|---|---|---|
| Composio Google Calendar | `executive-assistant`, `ea-book`, `ea-briefing` | Event listing, free slots, event creation, free/busy queries |
| Composio Gmail | `ea-briefing` | Email fetching, triage, previous exchange lookup |
| Firecrawl | `ea-save-link` | Article/webpage scraping and content extraction |
| LinkedIn (built-in) | `ea-briefing` | Attendee background research via `search_linkedin_person` |

```
/datagen:add-mcps
```

Add at minimum **Composio Google Calendar** and **Composio Gmail**. Firecrawl and LinkedIn are available by default on DataGen.

### 5. Clone and enter this repo

```bash
git clone https://github.com/datagendev/executive-assistant.git
cd executive-assistant
```

### 6. Try it out

```
/ea-briefing        # Morning briefing
/executive-assistant # Check availability
/ea-book            # Book a meeting
/ea-todo            # Manage your todo list
```

### 7. Deploy as an email agent (optional)

```
/datagen:deploy-agent
```

This deploys the executive-assistant agent to DataGen and gives you back an email address. You can then email your agent directly to interact with it.

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
    ea-save-link/             # Save articles to raw/ for later reading
  context/
    ea-preferences.md         # User preferences, blocklists, triage rules
scripts/
  save_link.py                # SDK script to fetch and save articles (token-efficient)
raw/                          # Saved articles and content
todo.md                       # Local task tracker (Now/Next/Later/Done)
```

## Customization

Edit `.claude/context/ea-preferences.md` to configure:
- Email blocklist (senders to skip in briefings)
- Email triage rules (what counts as urgent vs FYI)
- Todo format preferences
- Calendar timezone and working hours

## Next steps

- **Save-link skill** -- email a link to your agent and it fetches, parses, and saves the raw content to `/raw`. Build a personal read-it-later pipeline without leaving your inbox.

## License

MIT
