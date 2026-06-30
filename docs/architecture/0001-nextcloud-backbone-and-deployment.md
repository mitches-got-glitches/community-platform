# ADR-0001: Nextcloud backbone, deployed via Ansible-managed All-in-One

- **Status:** Accepted
- **Date:** 2026-06-18
- **Deciders:** Technical admin

## Context
We need a file store, wiki, task tracker, and shared calendar in one coherent system,
on infrastructure we control, reproducible from code, and operable by a single admin
(bus factor 1). Nextcloud covers four of the six required features natively: file
store + sync/share, wiki (Collectives app), task tracker (Deck app), and calendar
(CalDAV). It is the obvious backbone.

The real question was *how* to deploy it. Three routes were costed:

1. **AIO, manual setup** (~½ day): run the `nextcloud/all-in-one` master container by
   hand, configure via its web UI. ~80% reproducible (UI tweaks + volume state not in git).
2. **Ansible deploys AIO** (~1–1.5 days): a playbook provisions a bare VPS → installs
   Docker → drops the AIO compose + `.env` → configures Caddy. AIO still owns all internal
   container wiring and safe upgrades. ~95% reproducible (rebuild from bare VPS in one command).
3. **Ansible replaces AIO** (~3–6 days + permanent upgrade ownership): hand-roll
   Nextcloud-fpm + Postgres + Redis + Collabora + the Talk High Performance Backend
   (signaling + Janus + coturn/TURN) + backups + update orchestration. ~100% reproducible.

The expensive long tail in route 3 is exactly what AIO exists to solve: the Talk HPB/TURN
wiring (the most error-prone part of self-hosting Nextcloud), consistent DB+file backup
snapshots, and safe coordinated upgrades across ~6 interdependent containers — a burden
that recurs at every Nextcloud major release and lands entirely on the solo admin.

## Decision
Adopt **Nextcloud All-in-One** (`nextcloud/all-in-one`) as the deployment, **provisioned
and configured by an Ansible playbook** (route 2). Git-version the AIO `docker-compose.yml`,
the `.env`, the Caddy configuration, and the host-hardening tasks. Use **Caddy** as the
reverse proxy for automatic TLS (simpler single-file config than Traefik for one admin).

## Alternatives considered
- **Manual AIO (route 1):** rejected — weaker on the "code-first / reproducible" hard
  constraint with little effort saved over route 2.
- **Hand-rolled Compose + Ansible (route 3):** rejected — buys the last ~5% of
  reproducibility for ~3–5 extra days up front plus a permanent per-release upgrade
  burden, and produces the *worst* bus-factor story (a successor must understand bespoke
  roles and the TURN/HPB wiring rather than clicking "Update" in a UI). Overturns AIO
  for poor value at this scale.
- **Traefik instead of Caddy:** viable, but more configuration surface; Caddy's
  automatic HTTPS is the lower-maintenance choice for a solo admin.

## Consequences
- **Positive:** one-command rebuild from a bare VPS; AIO handles safe upgrades and
  Borg-based backups behind a UI a non-expert successor can operate; satisfies code-first
  to ~95%.
- **Negative / accepted:** AIO is semi-opinionated — post-install UI tweaks and Docker
  *volume* state are not captured in git. Mitigated by documenting UI steps in the
  restore runbook (see [0006](0006-backups-and-disaster-recovery.md)).
- The "code-first" constraint is honoured in spirit and ~95% in practice; we explicitly
  do **not** chase 100% via route 3.

## Conditions / follow-ups
- Verify arm64 image availability for all enabled AIO add-ons before committing to the
  ARM host — see [0005](0005-hosting-provider-and-sizing.md).
- Consider community automation (an Ansible role that deploys AIO) rather than writing
  the playbook entirely from scratch.
