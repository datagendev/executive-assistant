---
name: ea-todo
description: Manage local todo.md file. Use when user says "add to my todo", "what's on my list", "mark done", "update my tasks", or dumps a list of things to do.
---

# Todo Manager

Triage and manage tasks in the local `todo.md` file at the project root.

## File location

`./todo.md` in the project root.

## Format

```markdown
# Todo

## Now
<!-- High priority, do today -->
- [ ] Task description

## Next
<!-- Important but not urgent, do this week -->
- [ ] Task description

## Later
<!-- Backlog, nice to have -->
- [ ] Task description

## Done
<!-- Completed items, move here with date -->
- [x] Task description (completed 2026-04-08)
```

## Workflow

### Adding tasks

When the user dumps tasks (voice transcript, bullet list, or casual message):
1. Read current `todo.md`
2. Parse each task from the user's input
3. Triage into Now / Next / Later based on:
   - Explicit urgency ("urgent", "today", "asap") -> Now
   - Time-bound this week -> Next
   - Everything else -> Later
4. Add as `- [ ] Task description` under the right section
5. Show the user what was added and where

### Updating tasks

When user says "mark X done" or "finished X":
1. Read `todo.md`
2. Find the matching task
3. Change `- [ ]` to `- [x]`
4. Move it to the Done section with completion date
5. Show confirmation

### Reviewing tasks

When user says "what's on my list" or "show my todos":
1. Read `todo.md`
2. Display a clean summary with counts per section
3. Highlight any overdue or stale items in Now

### Reprioritizing

When user says "move X to Now" or "this is urgent now":
1. Read `todo.md`
2. Move the task to the requested section
3. Show confirmation

## Rules

- Always read `todo.md` before editing
- Preserve existing tasks when adding new ones
- When triaging ambiguous tasks, default to Next (not Now)
- Keep task descriptions concise but actionable
- Add completion date when marking done
- Never delete tasks, only move to Done
