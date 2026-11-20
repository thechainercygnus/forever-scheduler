---
name: ship-pr
description: Take finished work on a branch to a ready-to-review PR in this repo. Merge main, run the checks the change needs, commit with the sign-off and attribution, push, open the PR, note it on the roadmap, then watch CI and fix what fails. Use whenever a change is done and needs to go up, or more commits go onto an open PR.
---

# Ship a PR

CLAUDE.md's **Workflow** applies throughout:
- **Branch:** one branch per issue (`feature/<n>-<slug>`, or `fix/<slug>`), never `main`.
- **Commits:** one concern each, with an imperative subject.
- **Go-ahead:** commits and pushes need Bryce's. "Proceed", "go ahead" or "continue" on
  the task counts. Stop at a ready PR: Bryce merges.

## 1. Merge main first
Adding commits to an open PR? Check it's still open first:
`gh pr view <n> --json state --jq .state`. If it's merged, branch from `main` and open a
new PR.

```bash
git fetch origin main && git merge origin/main
```
Resolve any conflicts. If the remote branch has commits you don't have (an "Update branch"
on GitHub), pull and build on them. Never force-push.

## 2. Run the checks the change needs
Check what changed with `git diff --name-only origin/main...` plus the uncommitted files.

| Changed | Run |
|---|---|
| `src/`, `tests/`, `pyproject.toml` | `uv run ruff check --fix && uv run ruff format`, `uv run pyright`, `uv run pytest -q --cov` (the floor is in `pyproject.toml`) |
| `src/` | `uvx --from semgrep semgrep scan --error --config .semgrep/rules src`. The pre-push hook runs it too, at CI's pinned version. |
| `.semgrep/` | `uvx --from semgrep semgrep --test --config .semgrep/rules .semgrep/tests`, plus the scan |
| `.github/workflows/` | Actions pinned to a full SHA with `# vX.Y.Z`, and least-privilege `permissions:` |

When unsure, run everything. The `change-checklist` skill lists what else a kind of
change must touch.

## 3. Commit
Write the message to a file in the scratchpad and commit with `git commit -s -F <file>`.
Never skip the hooks: they rerun the checks.
```
<Imperative subject, under ~70 chars>

<Why, then what, wrapped at 72.>

Closes #<n>        (or Refs #<n>; leave it out for a fix with no issue)

<the attribution line the session's system reminder gives for commits>
```
`-s` adds the DCO sign-off (CONTRIBUTING.md). Take the attribution text from the current
system reminder; don't copy it from an old commit.

## 4. Push and open the PR
```bash
git push -u origin <branch>
gh pr create --base main --title "<title>" --body-file <file>
```
Add `--milestone <title>` when the issue has one. There's no PR template. Bodies follow
this shape:
```
Closes #<n>   (or Refs #<n>)

<One or two sentences: the problem and the result.>

## What changes
- **<Area>:** <what changes>

## Tests
- **<file or suite>:** <what it proves>

## Checks
- **<suite>:** <results>, with test counts
- **Merged `main` first.**
- **Not tested:** <anything only Bryce can check, such as the bot in a real server>

<the attribution line the session's system reminder gives for PR bodies>
```
Then use the `ccd_pr` tools: `get_status`, and `bind_pr` if the PR isn't bound.

## 5. Note it on the roadmap
Add `PR #<n>.` to the item's line on issue #4 (CLAUDE.md's **Roadmap**): write the body
to a file, edit it, and `gh issue edit 4 --body-file <file>`.

## 6. Watch CI and fix what fails
```bash
gh pr checks <n> --watch --interval 30 >/dev/null 2>&1; gh pr checks <n>
```
For a failing job, read its log:
```bash
gh api repos/thechainercygnus/forever-scheduler/actions/jobs/<job id>/logs | grep -E "Error|FAILED|assert"
```
The job id is the last number in the check's link. For CodeQL or Semgrep alerts, which
fail the check but don't show in the log:
```bash
gh api "repos/thechainercygnus/forever-scheduler/code-scanning/alerts?ref=refs/pull/<n>/merge&state=open" \
  --jq '.[] | {rule: .rule.id, path: .most_recent_instance.location.path, line: .most_recent_instance.location.start_line, msg: .most_recent_instance.message.text}'
```
- **The Semgrep secrets rule** follows taint through calls. Fix the code, or narrow the
  rule with a test in `.semgrep/tests`. Never disable it.
- **CodeQL** flags deliberate leaks in test fixtures when the source is named like a
  secret. Rename or restructure the fixture rather than dismissing the alert.

Fix on the branch, rerun step 2, merge `main` again, and push. Report what failed and
what fixed it.

## Windows shell
- **Heredocs:** they break on `'''`, `${...:-` and some quotes. Write files with the Write
  tool and run them; edit files with the Edit tool.
- **Stdin:** `gh` and `git` can wait on stdin from a Bash tool call. Add `< /dev/null`
  when a command doesn't read input.
- **Line endings:** Python's `write_text` writes CRLF on Windows. Use `write_bytes` when
  LF matters (issue bodies, fixtures).
