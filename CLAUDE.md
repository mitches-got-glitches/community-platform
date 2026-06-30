# CLAUDE.md — Community Org Self-Hosted Collaboration Stack

## Project overview
Self-hosted, sovereign, open-source collaboration stack for a small community
organisation (5–10 people now, sized for growth to ~20–30). Priorities: low budget,
data sovereignty, and being decoupled from big-tech platforms. Volunteer-run; one
technically capable admin (data/cloud infrastructure skills) — **bus factor is
currently 1**, and reducing it is an explicit design driver, not an afterthought.

## Hard constraints
- **Data sovereignty / UK GDPR is a baseline, not a feature.** Host on infrastructure
  we control. EU data residency is acceptable (UK–EU adequacy); prefer an EU/UK-owned
  provider to avoid US CLOUD Act / FISA 702 exposure (residency != sovereignty).
- **Low budget.** Working ceiling **~£250–300/yr**; realistic VAT-inclusive run-rate
  **~£230–280/yr** once hidden costs are counted (VAT, vault sharing, storage growth).
  (The original £100–150 was not achievable once off-site backups and a domain were
  counted; see `docs/architecture/0005`, `0006`, and the cost section of `docs/risks.md`.)
- **Not a registered nonprofit** — vendor nonprofit discounts (e.g. Proton) don't apply.
- **Code-first / reproducible.** Deployment is infrastructure-as-code, version-controlled.

## Required features
- Text chat: channels, channel membership, replies, threads
- Shared task tracker
- Wiki / knowledge base
- File store (sync + share)
- Voice/video chat
- Shared calendar (CalDAV, syncs to members' devices)

## Architecture (decided — see ADRs)
**Nextcloud is the backbone** — file store, wiki (Collectives), task tracker (Deck),
and calendar (CalDAV). Deployed via **Nextcloud All-in-One** (`nextcloud/all-in-one`),
**provisioned by an Ansible playbook** (Ansible deploys AIO; AIO owns the internal
container wiring and safe upgrades). Reverse proxy: **Caddy** (automatic TLS).

| Area | Decision | ADR |
|------|----------|-----|
| Backbone + deployment | Nextcloud AIO, deployed by Ansible; Caddy reverse proxy | [0001](docs/architecture/0001-nextcloud-backbone-and-deployment.md) |
| Chat | **Nextcloud Talk now**; Matrix + WhatsApp bridge deferred to Phase 2, **managed** | [0002](docs/architecture/0002-chat-layer.md) |
| Voice/video | **Talk + High Performance Backend**; Jitsi only if quality disappoints | [0003](docs/architecture/0003-voice-video.md) |
| Identity / SSO | **Deferred** — per-user accounts per service, no SSO yet | [0004](docs/architecture/0004-identity-and-sso.md) |
| Hosting | **Hetzner CAX31** (8 vCPU ARM / 16 GB / 160 GB, EU), sized for 20–30 | [0005](docs/architecture/0005-hosting-provider-and-sizing.md) |
| Backups / DR | AIO BorgBackup → **BorgBase** (EU, off-site); prune policy; tested restore | [0006](docs/architecture/0006-backups-and-disaster-recovery.md) |
| Secrets | **Proton Pass** shared vault, off the infrastructure it protects | [0007](docs/architecture/0007-secrets-management.md) |
| Operational baseline | EU SMTP relay, Healthchecks + uptime monitor, host hardening | [0008](docs/architecture/0008-operational-baseline.md) |
| Bus factor | Launch solo; **2nd admin onboarded ≤3 months**; launch blockers below | [0009](docs/architecture/0009-bus-factor-and-second-admin.md) |

## Cost summary (realistic, VAT-inclusive)
| Item | £/yr | Note |
|------|------|------|
| Hetzner CAX31 VPS | ~145 | **+ ~19% VAT (~£30) — not reclaimable (not VAT-registered)** |
| VAT on EU services | ~30–40 | the biggest quiet cost; base figures were ex-VAT |
| Off-site backup (BorgBase) | 0–20 | free <10 GB; ~£20 for 100 GB tier |
| Proton Pass shared vault | 24–50 | free tier sharing limits likely require Pass Plus/Business |
| Domain (EU registrar) | ~12–15 | renewal may exceed first-year teaser |
| File-storage growth | 0–80 | **sleeper** — media/photos can need a Hetzner volume or bigger box |
| FX + card fees | ~10–15 | costs in EUR/USD against a GBP budget |
| SMTP relay / monitoring | ~0 | free tiers (Scaleway TEM/Mailjet, Healthchecks) |
| **Realistic total** | **~£230–280** | thin headroom under the £250–300 ceiling |

**Excluded from the £-number (but the largest real cost):** the admin's volunteer time —
~days/weeks to build, then ~2–5 hrs/month ongoing. See `docs/risks.md`.

**Phase 2 funding gap:** the slack we assumed would fund managed Matrix is largely
consumed by these hidden costs. If Matrix/bridge becomes a real need, treat it as a
**committee budget-increase conversation**, not something that fits the current envelope.

## Launch blockers (non-negotiable before any production data)
1. **Proton Pass vault populated** with VPS root, registrar, and the **Borg backup key**
   — credentials must survive the admin even before a second admin exists.
2. **Restore runbook written and test-restored** against a fresh box — an untested
   backup is not a backup.
3. **Backup-failure alerting live** (Healthchecks.io on the Borg cron) — silent backup
   failure is the classic self-hosting disaster.

## Post-launch obligations
- **2nd admin onboarded within 3 months of go-live** (vault access + walked through a
  restore). If a second volunteer proves unrealistic, reopen [0009] and reconsider
  managed-ops for the operational continuity. Bus factor 1 is a launch state, not a
  steady state.

## Verify before building
- Confirm **arm64 images** exist for every AIO add-on you enable (Collabora, Talk HPB,
  recording). If a critical one is x86-only, fall back to Hetzner CPX31 (x86) — see [0005].
- Confirm current **Proton Pass free-tier vault-sharing limits**; a low-cost paid plan is
  fine within budget — see [0007].
