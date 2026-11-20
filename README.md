# Forever Scheduler

A Discord bot for scheduling WoW Forever dungeon and raid groups. It's planned to read who's
ready for what from the [Character Planner](https://github.com/thechainercygnus/character-planner),
through its integration API (character-planner#265), once that exists.

Early skeleton: the bot connects and answers `/ping`. Nothing is scheduled yet.

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

Decisions are recorded in [`docs/adr/`](docs/adr/). See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[AGPL-3.0-or-later](LICENSE).
