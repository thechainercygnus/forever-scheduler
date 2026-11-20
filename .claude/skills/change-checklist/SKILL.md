---
name: change-checklist
description: What else a change to this repo has to touch, by kind of change. A new command or plugin, table or column, setting, stored data, planner data shown in Discord, a DM, or a lasting decision. Use while planning or before shipping a change, so the migration, privacy note, tests and the rest aren't found missing in review or CI.
---

# Change checklist

Find each kind of change you're making, and do every line.

## A new slash command, button or plugin
- **Plugin:** one module per feature, its `arc.GatewayPlugin` added in `bot.build()`.
  `tests/test_bot.py`'s command names list grows with it.
- **Tests:** call the command's callback with a stand-in context, as
  `test_ping_responds_with_latency` does. Never connect to Discord.
- **Who may do it:** a member acts only for themself; changing or cancelling an event is
  for its creator (and server admins, once decided). Test the refusal too.
- **Replies:** ephemeral when only the member needs to see them.

## A new table or column (ADR 0002)
- **Migration:** an Alembic migration in the same PR, `batch_alter_table` for SQLite. The
  parity test must pass.
- **Retention:** every table is covered by the clean-up: events and sign-ups 30 days after
  the start, and a server's rows when the bot leaves it. Test both.
- **No Blizzard data:** nothing from the planner is stored (ADR 0002 decision 4). Keeping
  any of it needs a new ADR first.

## A new setting (`config.py`)
- **Secrets** are `SecretStr`, never logged, printed or sent to Discord. The Semgrep rule
  in `.semgrep/` catches `get_secret_value()` reaching a log, print, exception or
  message; a new kind of secret source gets a rule line and a test case.
- **Validate** anything used in a URL or path (`field_validator`).
- **Document it** in `.env.example`, commented out, with the issue and ADR.
- **Tests** build `Settings` with `_env_file=None`, never reading `.env`.

## Something that stores or shows personal data
- **Discord ids and sign-ups** are personal data: say what's kept, for how long and how
  to remove it in the README's privacy note (ADR 0002's consequences).
- **Planner data** (characters, specs, item levels, readiness) is shown only to members
  who opted in on the planner, and only in the server it belongs to
  (character-planner ADR 0034). Test with a member who didn't opt in.

## A direct message
- Only to members who share a server with the bot, only with their consent, and only what
  they turned on (character-planner ADR 0043).
- A refused DM (50007 or another 403) isn't retried: mark the member unreachable. Test it.

## Planner integration API (character-planner#265)
- Follow its published schema; never invent a field. Mock HTTP in tests; never call the
  planner.
- The token goes in an `Authorization: Bearer` header, never a URL.

## A new module, or a lasting decision
- **ADR:** add one in `docs/adr/`, numbered, short and terse. Bryce's choices go in as
  "Bryce chose ... (date)".
- **CLAUDE.md's Layout:** add a line for a new module.
- **New dependency:** check its current release first, and its license against
  `.github/dependency-review-config.yml`.

Then ship it with `ship-pr`.
