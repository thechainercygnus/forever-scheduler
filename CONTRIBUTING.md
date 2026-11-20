# Contributing

Thanks for your interest. This is a small hobby project with one maintainer, so reviews are
best effort. The rules below keep changes easy to review.

Everyone taking part follows the [code of conduct](CODE_OF_CONDUCT.md).
[GOVERNANCE.md](GOVERNANCE.md) says who decides what and how decisions are recorded.

## Proposing a change

1. **Open an issue first**, unless the change is a small fix. Say what you want to change
   and why. The [roadmap (#4)](https://github.com/thechainercygnus/forever-scheduler/issues/4)
   shows what's planned and in what order.
2. **One branch per issue**, from an up-to-date `main`: `feature/<issue>-<slug>`, or
   `fix/<slug>` for a small fix without an issue.
3. **Keep changes small.** One concern per commit, with an imperative subject
   ("Add event sign-ups", not "Added sign-ups").
4. **Open a pull request.** Write `Closes #<issue>` when it completes the issue, or
   `Refs #<issue>` when it's part of one.
5. **CI must pass** before merging: the `check` and `secret-scan` jobs and CodeQL's
   `analyze` jobs. A red job blocks the merge, even when it looks unrelated.

Decisions with lasting consequences get a short, numbered ADR in [`docs/adr/`](docs/adr/).

## Sign off your commits (DCO)

Every commit must be signed off under the [Developer Certificate of
Origin](https://developercertificate.org/). The sign-off says you wrote the change, or
have the right to submit it, under this project's license (AGPL-3.0-or-later).

```
git commit -s
```

This adds a `Signed-off-by: Your Name <you@example.com>` line matching your git identity.
To sign off commits you already made on your branch: `git rebase --signoff main`.

## Tests

- New or changed behaviour comes with tests.
- A bug fix comes with a regression test that fails without the fix.
- Tests never connect to Discord, call the Character Planner, or read `.env` (build
  `Settings` with `_env_file=None`).
- The planner is read only through its integration API (character-planner#265). Don't
  invent fields: follow its published schema.

## Coding standards

CI enforces these, and the pre-commit hooks run them locally:

- **Python** follows [PEP 8](https://peps.python.org/pep-0008/), checked by
  [Ruff](https://docs.astral.sh/ruff/), and is formatted by `ruff format` (Black's style,
  100-character lines). Types are checked by [pyright](https://microsoft.github.io/pyright/),
  strictly for `src/`. Settings are in `pyproject.toml`.
- Never log or print the Discord bot token or the planner's integration token. A
  [Semgrep](https://semgrep.dev) rule in `.semgrep/` checks it.
- Never commit `.env` or a database file: they hold secrets or members' data.
- GitHub Actions are pinned to a full commit SHA with the version as a comment, and each
  workflow job gets only the permissions it needs.

## Setting up and running the checks

You need [uv](https://docs.astral.sh/uv/). Then:

```
uv sync
uv run pre-commit install
```

The hooks then run on every commit, and the custom Semgrep rules run before every push
(they need uv's `uvx`). To run the full check by hand:

```
uv run ruff check --fix && uv run ruff format
uv run pyright
uv run pytest --cov
```

The custom Semgrep rules live in `.semgrep/`, each with test cases, and run in CI. To run
them locally:

```
uvx --from semgrep semgrep --test --config .semgrep/rules .semgrep/tests
uvx --from semgrep semgrep scan --error --config .semgrep/rules src
```

Coverage is measured in CI and shown in each run's summary. Its floor is `fail_under` in
`pyproject.toml`: a change that lowers coverage below it fails CI, so add tests with new
code. When coverage grows, raise the floor; never lower it to pass.

The [README](README.md) covers running the bot; you need a Discord application for that,
but not for the tests.

## Security issues

Don't open a public issue for a vulnerability. Report it privately as described in
[SECURITY.md](SECURITY.md).

## License

By contributing, you agree that your contribution is licensed under the
[AGPL-3.0-or-later](LICENSE), like the rest of the project.
