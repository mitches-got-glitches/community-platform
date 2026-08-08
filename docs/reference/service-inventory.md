# Service & vendor inventory

Every service the org depends on: what it does, who runs it (and where), what it costs, who owns the relationship, and where its credentials live. The core bus-factor + budget artifact — a second admin should be able to reconstruct the estate from this table. Keep it current; `TODO` = confirm.

| Service | Purpose | Vendor / jurisdiction | ~Cost/yr | Renewal | Owner | Creds | DPA | Status |
|---|---|---|---|---|---|---|---|---|
| Collaboration (Nextcloud) | files, wiki, tasks, calendar, chat | **IONOS** (🇩🇪) — pilot; likely **The Good Cloud** (🇳🇱) for prod | £1/mo→£9/mo (pilot) | 30-day refund; then 12-mo term | admin | Vault | **TODO — before real data** (R-26) | **real-data soft-launch pilot** ([ADR-0012](../architecture/0012-diy-vs-managed-nextcloud.md)) |
| Secrets vault | "BAFZ Vault" — org credentials | **Proton Pass Family** (🇨🇭) | £38–47 | TODO | admin | — (is the vault) | n/a | in use (2026-07-26) ([ADR-0007](../architecture/0007-secrets-management.md)) |
| Email mailboxes | `@bafz.org` human mail | **Migadu** (🇨🇭) | £15–70 (Mini likely) | TODO | admin | Vault | TODO | planned; migrating from live Proton ([ADR-0011](../architecture/0011-custom-domain-email-via-migadu.md)) |
| Outreach CRM | member/supporter CRM, canvassing, mass email | **Qomon** (🇫🇷) | existing | TODO | admin | Vault | **TODO** (R-28) | in use |
| Primary domain | `bafz.org` — org identity | registrar **TODO** — **not org-controlled** (R-29) | £12–15 | TODO | **external admin** | **not in vault** (R-29) | n/a | needs org control before prod |
| Video (fallback) | group calls >10 | self-hosted **Jitsi** (EU) / `meet.jit.si` (8x8 🇺🇸, casual only) | £0–100 | n/a | admin | Vault | n/a | fallback only ([ADR-0003](../architecture/0003-voice-video.md)) |
| Off-site backup | Nextcloud backup (DIY path) | **BorgBase** (🇩🇪) | £0–20 | TODO | admin | Vault + Borg key | n/a | DIY-on-trigger only; on managed = own-copy sync ([ADR-0006](../architecture/0006-backups-and-disaster-recovery.md)) |
| Compute (DIY-on-trigger) | Nextcloud host if self-hosted | **Netcup** (🇩🇪) | ~£198 | TODO | admin | Vault | TODO | on-trigger target ([ADR-0005](../architecture/0005-hosting-provider-and-sizing.md)/[0010](../architecture/0010-vps-provisioning-via-opentofu.md)) |
| Monitoring | uptime + backup alerts | **Healthchecks.io** | £0 | n/a | admin | Vault | n/a | planned ([ADR-0008](../architecture/0008-operational-baseline.md)) |
| Transactional relay | Nextcloud system mail | Scaleway TEM / Mailjet (EU) | £0 | TODO | admin | Vault | TODO | planned; may be moot on managed ([ADR-0008](../architecture/0008-operational-baseline.md)) |

**TODO:** confirm the registrar for `bafz.org` and who holds it; add renewal dates once accounts are set up; sign/record DPAs for every processor of member data (Nextcloud provider, Migadu, Qomon) before go-live.
