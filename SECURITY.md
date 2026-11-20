# Security policy

## Reporting a vulnerability

Please report security problems **privately**, not in a public issue:

- Use **Report a vulnerability** on this repository's
  [Security tab](https://github.com/thechainercygnus/forever-scheduler/security/advisories/new)
  (GitHub's private vulnerability reporting).

Include what you found, how to reproduce it, and what an attacker could do with it. Don't
include real tokens, secrets or personal data. If you need to show one, use a made-up
value.

This is a hobby project with one maintainer, so responses are best effort. I aim to
acknowledge a report within a week and to fix confirmed problems in the next release.

## What happens to a report

1. **Acknowledge.** I reply on the private advisory within a week, to say I've seen it.
2. **Assess.** I reproduce it and agree the impact with you, in the advisory. If it isn't
   a vulnerability, or it's out of scope (below), I say why and close it.
3. **Fix.** The fix is prepared privately, in the advisory's temporary fork where
   possible, with a test that fails without it.
4. **Release.** The fix ships in a new release. Its pull request carries the `security`
   label.
5. **Publish.** The advisory is published with the affected and fixed versions, and a
   CVE when GitHub assigns one.
6. **Credit.** You're credited in the advisory and the release notes, by the name or
   handle you choose, unless you ask not to be.

Please keep the details private until the advisory is published. If a fix will take
longer than the next release, I'll tell you in the advisory and agree a date with you.

## Supported versions

The latest release, and `main`. Fixes aren't backported to older versions.

## In scope

The code in this repository: the bot (`src/`) and the CI workflows. Examples:

- The Discord bot token or the planner's integration token leaking into logs, messages
  or errors.
- One Discord server's events or sign-ups shown in another, or a member's planner data
  shown to someone who didn't opt in (character-planner ADR 0034).
- Someone acting for another member: signing them up, withdrawing them, or changing an
  event they don't run.
- The bot sending DMs nobody consented to, or retrying refused ones (character-planner
  ADR 0043).
- Weaknesses in the workflows, such as untrusted input reaching a `run:` step.

## Out of scope

- Discord itself, and the Character Planner (report that to
  [its repository](https://github.com/thechainercygnus/character-planner/security)).
- A self-hosted copy's own setup, for example a leaked `.env` or bot token.
- Rate limiting or denial of service against a single self-hosted bot.
