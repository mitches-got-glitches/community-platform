# Managed-hosting limitations register

What we **cannot do** on managed Nextcloud that we could on a self-hosted box, what it has actually cost us, and what substitutes. Seeded from the IONOS pilot.

This is the evidence base for **exit trigger (1)** in [ADR-0012](../architecture/0012-diy-vs-managed-nextcloud.md) — *"a required feature hits the managed wall"*. Individually these are annoyances; the register exists so we notice when they add up to a decision. Record the observed cost, not the theoretical one — a limitation nobody has hit is not evidence.

## Limitations

| Limitation | Observed impact | Substitute | First seen |
|---|---|---|---|
| **No `occ` / shell access** | the umbrella cause of most rows below | OCS REST API for some of it (see next section) | 2026-08 |
| — `notification:test-push` unavailable | **iOS push cannot be tested at all** — no in-app diagnosis on iOS either, so an iPhone-only report can be narrowed but never confirmed ([talk-notifications](../runbooks/talk-notifications.md)) | provider ticket | 2026-09-22 |
| — no server log access | a failed push, or mail that never arrives, cannot be diagnosed from our side | provider ticket | 2026-09-22 |
| — no `config:system:set` | config limited to what the admin UI exposes | none | 2026-08 |
| — no `files:scan` | files placed outside Nextcloud are not picked up — **relevant to the own-copy sync**, which must therefore be one-way (pull), never a write-back path | keep sync read-only | 2026-08 |
| — no maintenance mode / app-upgrade control | cannot quiesce the instance for a clean backup snapshot | none | 2026-08 |
| **No control of the Nextcloud version** | **Talk threads — a required feature — were unavailable for ~12 months.** Upstream Hub 25 "Autumn" shipped 2025-09; reached our instance ~2026-09 | wait, or leave | 2026-08 → resolved 2026-09-22 |
| **No clean export** | migration off is per-app (files via sync copy, calendars `.ics`, contacts `.vcf`, Deck JSON, Collectives markdown) and **Talk history is sacrificed** | day-one own-copy sync as migration insurance ([ADR-0006](../architecture/0006-backups-and-disaster-recovery.md)) | 2026-08 |
| **No SLA / uptime guarantee; data-loss liability disclaimed** | backups are entirely our responsibility despite not running the box | own-copy sync — mandatory, not optional | 2026-08 |

## What the OCS REST API covers instead

Reachable over HTTPS with an app password, so it survives the absence of `occ` — this is what keeps the [code-first constraint](../architecture/0012-diy-vs-managed-nextcloud.md) partially alive on managed hosting.

| Area | Endpoint |
|---|---|
| Users & groups (DOC-4) | `/ocs/v1.php/cloud/users` |
| Talk | `/ocs/v2.php/apps/spreed/api/v4/...` |
| Deck | `/index.php/apps/deck/api/v1.0/boards` |
| Collectives | `/index.php/apps/collectives/_api` |
| Files | WebDAV — `/remote.php/dav/files/<user>/` |
| Calendar / contacts | CalDAV / CardDAV |

**TODO:** confirm IONOS does not restrict API access — untested as of 2026-09-22.

**Not covered by the API**, and therefore provider-ticket-only: maintenance mode, app upgrades, `config.php`, file rescans, server logs, and push diagnostics.

## How to use this register

- **Add a row when a limitation costs real time or blocks a real task** — dated, with what actually happened.
- **Review before the provider decision** and at each pilot decision gate ([pilot runbook](../runbooks/managed-nextcloud-pilot.md)).
- A row that turns out to be wrong (or gets resolved upstream) is **marked resolved with the date**, not deleted — the pattern over time is the point.
