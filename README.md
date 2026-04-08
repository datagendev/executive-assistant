# Executive Assistant for Claude Code

A personal executive assistant built as a Claude Code agent with modular skills. Manages your calendar, email triage, todo list, and morning briefings with meeting prep.

Built with [DataGen](https://datagen.dev) for tool orchestration via Composio integrations (Google Calendar, Gmail, LinkedIn).

## What it does

- **Morning briefing** -- today's schedule, todos, email highlights, and deep meeting prep with LinkedIn background research on attendees
- **Calendar availability** -- show free time slots, copy-pasteable for sharing
- **Book meetings** -- find free slots, create events with attendees
- **Todo management** -- triage tasks into Now/Next/Later, track completion in a local `todo.md`

## Setup

1. Install [Claude Code](https://claude.ai/code)
2. Clone this repo
3. Run `/datagen:setup` to connect DataGen
4. Connect Composio Google Calendar and Gmail in your DataGen dashboard
5. Run `/ea-briefing` for your first morning briefing

## License

MIT
