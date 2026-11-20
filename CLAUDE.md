# CLAUDE.md

Instructions for AI coding agents working in this repo.

## What this is

A Discord bot for scheduling WoW Forever dungeon and raid groups, built on hikari and
hikari-arc. It's a companion to the Character Planner
(`thechainercygnus/character-planner`), which it will read through the planner's
integration API (character-planner#265). See `docs/adr/0001-separate-project.md`.

## Commands

All tooling runs through uv. Run the full check before calling any change done:

```
uv sync
uv run ruff check --fix && uv run ruff format
uv run pyright
uv run pytest --cov
```

Run the bot: `uv run forever-scheduler` (needs `.env` with `DISCORD_TOKEN`).

## Rules

- Every behaviour change gets a test. Tests never connect to Discord, call the planner,
  or read `.env` (build `Settings` with `_env_file=None`).
- Never log or print the Discord token or the planner token.
- Never commit `.env`.
- Read the planner's data only through its integration API, never its database. Don't
  invent fields: follow the API's published schema.
- Planner data shown in Discord is Blizzard data: show it only to the members who opted in,
  and don't keep it longer than the planner's rules allow (character-planner ADR 0034).
- A bot only DMs people it shares a server with, and only with their consent; a refused DM
  isn't retried (character-planner ADR 0043).
- Pin GitHub Actions to a full commit SHA with the version as a comment. Give each workflow
  job only the permissions it needs.
- Record decisions with lasting consequences as a new, short, numbered ADR in `docs/adr/`.
- Before adding a dependency, check its current release; don't pin a remembered version.

## Workflow

- One branch per issue, `feature/<issue>-<slug>` or `fix/<slug>`, from an up-to-date
  `main`. Never commit or push to `main`.
- Before opening or updating a PR, merge `origin/main` and rerun the checks.
- Commits are signed off (`git commit -s`) and need the user's go-ahead. Stop at a
  ready-to-review PR; the user merges.

## Layout

- `src/forever_scheduler/bot.py`: builds the hikari bot and arc client; `main()` runs it.
- `src/forever_scheduler/config.py`: settings from the environment.
- `src/forever_scheduler/commands.py`: the core plugin (`/ping`). Each feature gets its own
  plugin module, added in `bot.build()`.
