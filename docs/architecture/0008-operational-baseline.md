# ADR-0008: Operational baseline — SMTP, monitoring, host hardening

- **Status:** Accepted
- **Date:** 2026-06-18
- **Deciders:** Technical admin

## Context
Three operational essentials were missing from the original plan. Each is exactly the kind
of thing a solo admin gets burned by, so they are recorded as first-class decisions, not
afterthoughts.

1. **Outbound email (SMTP).** Nextcloud *needs* it — password resets, share notifications,
   and calendar invites silently fail without it. Self-hosting outbound mail is a
   deliverability and maintenance nightmare (reputation, SPF/DKIM/DMARC, blocklists).
2. **Monitoring + backup-failure alerting.** A silent backup failure is *the* classic
   self-hosting disaster — discovered on the day you need the backup, three months too late.
   A solo admin also needs to know when the box is down.
3. **Host OS security.** AIO patches the *containers*, not the *host*. The VPS itself needs
   hardening and unattended security updates.

## Decision
1. **SMTP:** use a **cheap EU transactional relay** (e.g. Scaleway TEM or Mailjet/FR) for
   Nextcloud's outbound mail. Reliable deliverability, sovereign, ~free at our volume. Do
   not self-host outbound mail. (If the org already has a suitable mailbox/SMTP, reusing it
   is acceptable.)
2. **Monitoring:** **Healthchecks.io** pings the Borg backup cron (alerts on a *missed*
   backup) **plus a lightweight external uptime monitor** for the box. Both have free tiers.
   The monitor must be **external** — monitoring that runs on the same box can't tell you
   the box is down.
3. **Host hardening:** **baked into the Ansible playbook** — `unattended-upgrades`
   (automatic OS security patches), keys-only SSH (no password auth), a firewall (UFW)
   exposing only 80/443/SSH, and `fail2ban`. Reproducible, done once, fits the IaC approach
   ([0001](0001-nextcloud-backbone-and-deployment.md)).

## Alternatives considered
- **Self-hosted outbound mail:** rejected — deliverability burden far outweighs the cost of
  a relay.
- **Self-host Uptime Kuma on the box:** rejected as the *primary* monitor — can't detect
  its own host being down. Fine as a secondary internal dashboard.
- **Manual host hardening:** rejected in favour of playbook-encoded hardening for
  reproducibility and successor-operability.

## Consequences
- **Positive:** notifications/resets work; backup failures are loud and early; the host is
  patched and locked down reproducibly.
- **Negative / accepted:** dependencies on a couple of free-tier external services
  (Healthchecks, SMTP relay) — credentials go in the Proton Pass vault ([0007]).

## Conditions / follow-ups
- **Launch blocker:** backup-failure alerting must be live before production data (see
  CLAUDE.md).
- Confirm the SMTP relay's free-tier sending limits cover expected notification volume.
