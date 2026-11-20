# 0001: A separate project, on hikari and hikari-arc

Status: accepted (2026-11-19)

## Context

Bryce wants a Discord bot to schedule dungeon and raid groups, linked to the Character
Planner and other WoW Forever tools. The planner's own Discord features only make
outgoing calls: bot DMs (planner ADR 0043), a pinned sign-up message (ADR 0048), and a
guild channel webhook (ADR 0046). A scheduler needs slash commands and buttons, so a
gateway connection that stays open.

## Decision

1. **Its own repo, Discord application and deployment.**
   - It's a different domain (events, sign-ups by role, time zones, reminders), with
     different users: raiders don't all need planner accounts.
   - A self-hosted planner stays one image with nothing extra to run (planner ADR 0020).
   - Its own Discord application can be installed or revoked apart from the planner's bot.
2. **It reads the planner through an integration API** (character-planner#265): scoped
   tokens, with each member opting in. It never reads the planner's database.
3. **Python, with the planner's tooling** (uv, ruff, pyright strict on `src`, pytest with
   warnings as errors), so the two repos work alike.
4. **hikari for the gateway, hikari-arc for commands** (Bryce, 2026-11-19).
   - hikari is typed and supports Python 3.14.
   - arc's commands are typed, which suits pyright strict, and are grouped in plugins, one
     per feature.

## Consequences

- Two deployments to run where one did. The planner's Discord DMs could move to this bot
  later; that's a decision for then.
- What it can show from the planner depends on #265's reading of Blizzard's terms
  (planner ADR 0034).
