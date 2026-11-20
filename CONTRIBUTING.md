# Contributing

A small hobby project with one maintainer, so reviews are best effort.

## Proposing a change

1. **Open an issue first**, unless it's a small fix.
2. **One branch per issue** from an up-to-date `main`: `feature/<issue>-<slug>`, or
   `fix/<slug>` for a small fix.
3. **Keep changes small.** One concern per commit, with an imperative subject.
4. **Open a pull request** with `Closes #<issue>` or `Refs #<issue>`. CI must pass.

Decisions with lasting consequences get a short, numbered ADR in [`docs/adr/`](docs/adr/).

## Sign off your commits (DCO)

Every commit is signed off under the [Developer Certificate of
Origin](https://developercertificate.org/): `git commit -s`.

## Tests and standards

- New or changed behaviour comes with tests. Tests never connect to Discord or the
  planner, and never read `.env`.
- Ruff checks and formats Python (100-character lines); pyright checks types, strictly for
  `src/`. Settings are in `pyproject.toml`; the pre-commit hooks run them.
- Never log or print the Discord token or the planner token.
