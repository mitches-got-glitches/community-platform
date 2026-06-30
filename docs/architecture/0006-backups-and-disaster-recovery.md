# ADR-0006: Backups and disaster recovery

- **Status:** Accepted
- **Date:** 2026-06-18
- **Deciders:** Technical admin

## Context
A single VPS is a single point of failure for availability, so backups are the real
continuity story — and they're doubly important for a bus-factor-1 org. Nextcloud AIO
ships **BorgBackup** built in: it dumps the database and snapshots the volumes
*consistently*, then encrypts the archive with a Borg key. What AIO does not decide is
**where the off-site copy goes**, which carries both a sovereignty and a bus-factor
dimension.

Expected data size is small (a few GB to low tens of GB), and Borg deduplicates +
compresses, so the repo is often smaller than the source. That makes free/cheap EU tiers
viable.

Two traps specific to this use case:
- **The encryption key is a bus-factor item.** If only the admin holds the Borg key and
  the admin is gone, the off-site backups are unrecoverable — backups nobody can open.
- **An untested backup is not a backup.** Without a test restore against a fresh box, we
  don't actually know we have a recoverable system.

## Decision
- **Engine:** AIO's built-in BorgBackup.
- **Off-site target:** **BorgBase free tier (10 GB, EU/Germany)** — native Borg, near-zero
  friction with AIO, different vendor from Hetzner (so it's genuinely off-site). Upgrade to
  the ~£20/yr 100 GB tier if/when we exceed 10 GB.
- **Retention:** a sane prune policy (e.g. 7 daily / 4 weekly / 6 monthly) so history
  doesn't silently inflate the repo past the free tier.
- **Third copy:** a **quarterly manual cold export** the admin downloads and stores
  separately (cheap 3-2-1 third leg).
- **Key custody:** the **Borg key/passphrase lives in the Proton Pass shared vault**
  ([0007](0007-secrets-management.md)) from day one.
- **Alerting:** **Healthchecks.io** pings the Borg cron and alerts if a backup is missed
  ([0008](0008-operational-baseline.md)).
- **Runbook:** a written restore runbook, **test-restored against a fresh box before
  go-live**, covering the AIO UI-driven steps not captured in git ([0001]).

## Alternatives considered
- **Hetzner Storage Box:** cheap (~£40/yr) and native Borg, but **same vendor** as the VPS
  (account-level failure takes both) and its floor is 1 TB — no small/cheap tier. Rejected.
- **Scaleway Object Storage free tier (75 GB, EU/France):** more headroom, but S3 (needs
  `restic`, a second backup tool outside AIO's native Borg). Viable backup-2 option later.
- **Backblaze B2:** dirt cheap, but **US jurisdiction** (CLOUD Act) — undercuts the
  sovereignty stance even with client-side encryption. Rejected.
- **rsync.net:** Borg-friendly but pricier and weaker on sovereignty (CH/US). Rejected.

## Consequences
- **Positive:** true off-site, EU/sovereign, ~£0–20/yr; recoverable by a second admin
  because the key is in the shared vault; failure is *loud*, not silent.
- **Negative / accepted:** free tier ceiling (10 GB) requires watching the prune policy;
  recovery is a *rebuild-and-restore* (minutes-to-hours), not high availability — accepted
  at this budget.

## Conditions / follow-ups
- Restore test + alerting + key-in-vault are **launch blockers** (see CLAUDE.md).
- Re-test the restore after any major AIO upgrade.
