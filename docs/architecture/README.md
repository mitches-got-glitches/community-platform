# Architecture Decision Records

This directory records the significant decisions behind the community org's
self-hosted collaboration stack, and *why* each was made — so a future admin (or
the current one, six months from now) can understand the reasoning, not just the
outcome.

Each ADR follows a light format: **Context → Decision → Alternatives considered →
Consequences → Conditions/Follow-ups**. Status is one of `Proposed`, `Accepted`,
`Superseded`.

| ADR | Title | Status |
|-----|-------|--------|
| [0001](0001-nextcloud-backbone-and-deployment.md) | Nextcloud backbone, deployed via Ansible-managed AIO | Accepted |
| [0002](0002-chat-layer.md) | Chat: Nextcloud Talk now, Matrix later (managed) | Accepted |
| [0003](0003-voice-video.md) | Voice/video: Nextcloud Talk + High Performance Backend | Accepted |
| [0004](0004-identity-and-sso.md) | Identity: per-app accounts, SSO deferred | Accepted |
| [0005](0005-hosting-provider-and-sizing.md) | Hosting: Hetzner CAX31 (ARM), sized for 20–30 | Accepted |
| [0006](0006-backups-and-disaster-recovery.md) | Backups: AIO Borg → BorgBase, tested restore | Accepted |
| [0007](0007-secrets-management.md) | Secrets: Proton Pass shared vault | Accepted |
| [0008](0008-operational-baseline.md) | Operational baseline: SMTP, monitoring, host hardening | Accepted |
| [0009](0009-bus-factor-and-second-admin.md) | Bus-factor mitigation and second-admin policy | Accepted |
| [0010](0010-diy-vs-managed-nextcloud.md) | DIY vs Managed Nextcloud (reconsidering archetype C) | Proposed |

All decisions dated **2026-06-18**. Decider: the org's technical admin.

> Cross-cutting theme: **bus factor is currently 1.** Almost every decision below
> trades raw capability or cost for operability and recoverability by a single
> admin (and an as-yet-unrecruited second). When in doubt, the plan chose fewer
> moving parts.
