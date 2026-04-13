# Executive Assistant for Claude Code

A personal executive assistant built as a Claude Code agent with modular skills. Manages your calendar, email triage, todo list, morning briefings, content saving, and prospect meeting prep.

Built with [DataGen](https://datagen.dev) for tool orchestration via Composio integrations (Google Calendar, Gmail, LinkedIn, Fireflies, HeyReach).

https://github.com/datagendev/executive-assistant/releases/download/v0.1.0/showcase.mp4

## What it does

- **Morning briefing** -- today's schedule, todos, email highlights, and deep meeting prep with LinkedIn background research on attendees
- **Calendar availability** -- show free time slots, copy-pasteable for sharing
- **Book meetings** -- find free slots, create events with attendees
- **Todo management** -- triage tasks into Now/Next/Later, track completion in a local `todo.md`
- **Save links** -- save articles, YouTube transcripts, and LinkedIn posts to `raw/` for later reading
- **Prospect meeting prep** -- gather Gmail history, Fireflies transcripts, HeyReach messages, and LinkedIn profile/posts into a formatted brief

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
| Composio Gmail | `ea-briefing`, `ea-prep-prospect` | Email fetching, triage, previous exchange lookup |
| Firecrawl | `ea-save-link` | Article/webpage scraping and content extraction |
| Fireflies | `ea-prep-prospect` | Meeting transcript search and retrieval |
| HeyReach | `ea-prep-prospect` | LinkedIn conversation history |
| LinkedIn (built-in) | `ea-briefing`, `ea-prep-prospect` | Profile data, posts, person search |

```
/datagen:add-mcps
```

Add at minimum **Composio Google Calendar** and **Composio Gmail**. Firecrawl, Fireflies, HeyReach, and LinkedIn are available by default on DataGen.

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
/ea-save-link       # Save an article, YouTube video, or LinkedIn post
/ea-prep-prospect   # Prep for a prospect meeting
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
    ea-save-link/             # Save articles, YouTube, LinkedIn posts to raw/
    ea-prep-prospect/         # Prospect meeting prep with multi-source research
  context/
    ea-preferences.md         # User preferences, blocklists, triage rules
scripts/
  save_link.py                # Router: detects URL type and dispatches to the right script
  save_youtube.py             # Fetch YouTube transcripts via Supadata API
  save_linkedin_post.py       # Fetch LinkedIn posts via DataGen tools
raw/                          # Saved articles, transcripts, and posts
tmp/                          # Temporary research data for prospect prep briefs
todo.md                       # Local task tracker (Now/Next/Later/Done)
```

## Customization

Edit `.claude/context/ea-preferences.md` to configure:
- Email blocklist (senders to skip in briefings)
- Email triage rules (what counts as urgent vs FYI)
- Todo format preferences
- Calendar timezone and working hours

## License

MIT
