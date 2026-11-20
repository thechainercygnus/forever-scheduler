# 0002: Storage, data model and time zones

Status: proposed (2026-11-19)

## Context

The bot remembers nothing between restarts. Scheduling needs events and sign-ups that
outlive the process. ADR 0001 set the domain (events, sign-ups by role, time zones,
reminders) but not where it's kept or what may be kept. Two rules from the planner bear
on that: Blizzard data is kept at most 30 days and deleted when its owner opts out
(planner ADR 0034), and the planner's own storage is SQLModel with Alembic migrations
(planner ADR 0022).

## Decision

1. **SQLite by default, through SQLModel on SQLAlchemy's async engine.**
   - One bot process holds one gateway connection, so one writer: SQLite is enough. The
     file's location is a setting (`DATABASE_URL`, defaulting to a file next to the bot).
   - The async engine (`aiosqlite`) keeps database calls off the gateway's event loop.
   - SQLModel, as in the planner, so both repos model tables alike. Postgres stays
     possible by changing the URL, as it is for the planner.
2. **Alembic migrations from the first table,** following planner ADR 0022: migrations
   inside the package, `upgrade head` at every start, batch mode for SQLite, and a parity
   test that fails when a model changes without a migration.
3. **A small model, holding only what members type into Discord.**
   - `Event`: guild, channel and message ids, who created it, kind (dungeon or raid), the
     instance as free text, start time, group size, and created and cancelled times.
   - `Signup`: event, Discord user id, role (tank, healer or damage), and when they signed
     up. One sign-up per member per event; changing role updates it.
   - The planner's dungeon and raid names may later fill a picker, but the stored value
     stays the member's choice, not planner data.
4. **No planner or Blizzard data in the database.** Character names, specs, item levels
   and readiness are fetched from the planner's integration API (character-planner#265)
   when shown, and at most held in memory for minutes. So the 30-day limit and opt-outs
   are met by not storing anything, and an opt-out applies on the next view. If a later
   feature needs to keep any of it, that's a new ADR.
5. **Times stored in UTC, shown with Discord timestamps.**
   - Start times are timezone-aware datetimes, stored as UTC.
   - Discord shows `<t:…:F>` and `<t:…:R>` timestamps in each viewer's own time zone, so
     the bot never needs to know a viewer's zone to display a time.
   - Entering a time needs a zone: `/event create` takes an IANA zone name (via
     `zoneinfo`), with a per-server default to come later. The zone isn't stored with the
     event.
6. **Old data goes.**
   - Events and their sign-ups are deleted 30 days after their start time.
   - When the bot leaves a server, that server's events and sign-ups are deleted.
   - A member can withdraw a sign-up at any time, which deletes it.

## Consequences

- The first feature PR adds `sqlmodel`, `alembic` and `aiosqlite` (checking each one's
  current release then), the engine setup, the baseline migration and the parity test.
- Discord user ids are personal data, so the README gains a short note on what's kept,
  for how long, and how to remove it, as the planner's privacy notice does.
- Showing planner data means a call to the planner each time, so views with many members
  need the guild endpoint from #265 rather than one call per member.
- Running more than one bot process, or sharding, would mean moving to Postgres first.
