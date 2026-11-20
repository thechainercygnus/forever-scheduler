# CLAUDE.md

Instructions for AI coding agents working in this repo.

## What this is

A Discord bot for scheduling WoW Forever dungeon and raid groups, built on hikari and
hikari-arc. It's a companion to the Character Planner
(`thechainercygnus/character-planner`), which it will read through the planner's
integration API (character-planner#265). See `docs/adr/0001-separate-project.md`.

## Commands

All tooling runs through uv. Run the full check before calling any change done or pushing:

```
uv sync
uv run ruff check --fix && uv run ruff format
uv run pyright
uv run pytest --cov
```

Run the bot: `uv run forever-scheduler` (needs `.env` with `DISCORD_TOKEN`).
Custom Semgrep rules in `.semgrep/`: `uvx --from semgrep semgrep --test --config .semgrep/rules .semgrep/tests` tests them, and `uvx --from semgrep semgrep scan --error --config .semgrep/rules src` runs them, as CI's `semgrep` workflow does. The pre-push hook runs both at CI's pinned version (`tests/test_hooks.py` keeps the two in step).
Coverage: `uv run pytest --cov`. CI puts it in the run's summary and fails below the floor, `fail_under` in `pyproject.toml`. Raise it when coverage grows; never lower it to pass.

Project skills in `.claude/skills/` (Claude Code loads them): `ship-pr` takes finished work to a ready PR and watches its CI, and `change-checklist` lists what each kind of change must also touch.

## Rules

`CONTRIBUTING.md` holds the shared rules for everyone (workflow, tests, coding standards,
DCO sign-off). The rules here add what agents need on top.

- Every behaviour change gets a test. Tests never connect to Discord, call the planner,
  or read `.env` (build `Settings` with `_env_file=None`).
- Never log or print the Discord token or the planner token.
- Never commit `.env` or a database file.
- Read the planner's data only through its integration API, never its database. Don't
  invent fields: follow the API's published schema.
- Planner data shown in Discord is Blizzard data: show it only to the members who opted in,
  and don't store it (ADR 0002; character-planner ADR 0034).
- A bot only DMs people it shares a server with, and only with their consent; a refused DM
  isn't retried (character-planner ADR 0043).
- Pin GitHub Actions to a full commit SHA with the version as a comment
  (`uses: owner/action@<sha> # v1.2.3`). Give each workflow job only the permissions it
  needs. Dependabot keeps pins current.
- Record decisions with lasting consequences as a new, short, numbered ADR in `docs/adr/`.
- Before adding a dependency, check its current release; don't pin a remembered version.
- Keep changes small and on a branch; one concern per commit, imperative commit subjects.

## Workflow

- One branch per issue, named `feature/<issue>-<slug>` (or `fix/<slug>` for small fixes
  without an issue), from an up-to-date `main`. Never commit or push to `main`.
- Before opening a pull request, and before pushing more commits to an open one: fetch
  `main`, merge `origin/main` into the branch, resolve any conflicts, and rerun the full
  checks on the merged result. If the remote branch has commits you don't (an "Update
  branch" on GitHub), build on them; never force-push.
- Open a pull request for every branch. Use `Closes #<issue>` when it completes the issue
  and `Refs #<issue>` when it's part of one.
- CI must pass before merging: the `check` and `secret-scan` jobs and CodeQL's `analyze`
  jobs (the "Protect main" ruleset requires them). A red job is a blocker, even if it
  looks unrelated; fix it or say why in the PR.
- Sessions run in their own git worktree. Stay inside it: don't edit files in another
  checkout of this repo.
- Commits are signed off (`git commit -s`). Commits and pushes need the user's go-ahead.
  Stop at a ready-to-review PR; the user merges.

## Roadmap

Issue #4 (label `roadmap`) is the work order. Read it before choosing what to do next,
and keep it true as you go: edit its body with `gh issue edit 4 --body-file <file>`.

- Pick the first unchecked item under "Now" or "Next" that isn't parked or marked as the
  user's own task.
- When you open a PR for an item, note the PR number on its line. When it merges, check
  the box and say what's left, if anything, before the issue can close.
- When an issue closes, move its line to "Done".
- New issues go on the roadmap in the right place, with a one-line reason if it isn't the end.
- Reorder only when the user asks, or propose a change and wait for their answer.
- Keep the existing sections and their order. Write each item as `#<n> <title>` plus a
  short note. Don't change items you didn't work on.

## Layout

- `src/forever_scheduler/bot.py`: builds the hikari bot and arc client; `main()` runs it.
- `src/forever_scheduler/config.py`: settings from the environment.
- `src/forever_scheduler/commands.py`: the core plugin (`/ping`). Each feature gets its own
  plugin module, added in `bot.build()`.
- `docs/adr/`: decision records. `.semgrep/`: the repo's own Semgrep rules and their tests.
