# Forever Scheduler

[![ci](https://github.com/thechainercygnus/forever-scheduler/actions/workflows/ci.yml/badge.svg)](https://github.com/thechainercygnus/forever-scheduler/actions/workflows/ci.yml)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/thechainercygnus/forever-scheduler/badge)](https://scorecard.dev/viewer/?uri=github.com/thechainercygnus/forever-scheduler)

A Discord bot for scheduling WoW Forever dungeon and raid groups. It's planned to read who's
ready for what from the [Character Planner](https://github.com/thechainercygnus/character-planner),
through its integration API (character-planner#265), once that exists.

Early skeleton: the bot connects and answers `/ping`. Nothing is scheduled yet. What's
planned, in order, is on the [roadmap (#4)](https://github.com/thechainercygnus/forever-scheduler/issues/4).

**Related projects:** the [Character Planner](https://github.com/thechainercygnus/character-planner)
plans gear, talents and progression, and
[CharacterPlannerExport](https://github.com/thechainercygnus/character-planner-export)
feeds it in-game data.

## Run it

1. Create an application in the [Discord developer portal](https://discord.com/developers/applications),
   add a bot, and copy its token.
2. Invite the bot to a test server with the `bot` and `applications.commands` scopes.
3. Copy `.env.example` to `.env`, set `DISCORD_TOKEN`, and set `DEV_GUILD_IDS` to your test
   server's id so commands show up straight away.
4. Run it:

   ```
   uv sync
   uv run forever-scheduler
   ```

## Develop

```
uv run pre-commit install
uv run ruff check --fix && uv run ruff format
uv run pyright
uv run pytest --cov
```

CI runs the same checks plus a gitleaks secret scan, CodeQL, the custom Semgrep rules and,
on pull requests, Dependency Review. Decisions are recorded in [`docs/adr/`](docs/adr/).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md): issues first, a branch and pull request per issue,
tests with every change, and signed-off commits (DCO). [GOVERNANCE.md](GOVERNANCE.md)
covers who decides what, and everyone taking part follows the
[code of conduct](CODE_OF_CONDUCT.md).

## Security

Please report vulnerabilities privately. See [SECURITY.md](SECURITY.md), which also covers
how reports are handled and credited.

## License

Forever Scheduler is free software under the [GNU Affero General Public License v3.0 or
later](LICENSE). You may run, study, share and change it. If you run a modified version
for other people to use over a network, you must offer them its source code under the same
license.

The license covers this project's code only. World of Warcraft names and game data belong
to Blizzard Entertainment, and character data shown from the Character Planner comes from
Blizzard's Battle.net API under its developer terms (character-planner ADR 0034). Discord
is a trademark of Discord Inc. This project isn't affiliated with or endorsed by Blizzard
or Discord.
