# Phase 0 — Carry-forward pilot plan (2–5 users, 1–2 months)

A small, cheap pilot that **grows into production rather than being thrown away.** Because
the users are non-technical and we intend to keep the instance, the pilot is run as a
*smaller production instance*, not a separate throwaway — which is both cheaper and lower
risk than building twice.

Relates to: [ADR-0001](architecture/0001-nextcloud-backbone-and-deployment.md),
[ADR-0005](architecture/0005-hosting-provider-and-sizing.md),
[ADR-0006](architecture/0006-backups-and-disaster-recovery.md),
[`project-backlog.md`](project-backlog.md) (pilot-scope tasks tagged `pilot`).

## What the pilot validates
Three questions — not feature-completeness:
1. **Will people switch** from WhatsApp/Google for org business?
2. **Can the admin run it** without it eating their life?
3. **Where's the friction** — especially calendar/CalDAV sync and mobile apps?

## The one decision that shapes everything: commit to the real domain now
Changing Nextcloud's domain later is painful (it's baked into `overwrite.cli.url`, share
links, and every synced client). Since we're carrying forward, **register the final
production domain at the start** and run the pilot on it. This is also why we **do not use
Tailscale** for the pilot:

- Tailscale needs every user on a VPN app + account, runs as an always-on phone VPN (only
  one VPN allowed at a time), breaks CalDAV when disconnected, and does not scale to 20–30
  non-technical members. Good for a solo/technical dry-run; wrong as the access layer we
  grow.
- A **public domain + automatic TLS** gives non-technical users the Google-like experience
  they need: open a URL or the app, log in, done — no VPN, no extra account.

## Scope

| In scope (the MVP) | Out of scope (defer to full rollout) |
|--------------------|--------------------------------------|
| Files: sync + a couple of shared folders | Talk **HPB** group video (small calls are P2P) |
| Talk: 2–3 channels + a small video call | Matrix / WhatsApp bridge, SSO |
| **Calendar/CalDAV** — *test hardest* | Ansible IaC playbook (manual AIO for pilot) |
| Wiki (Collectives): 1–2 pages | Tested-restore runbook + backup alerting *(before full rollout)* |
| BorgBase backup from day one | Proton Pass vault formalisation *(before full rollout)* |
| Basic host hardening (public-facing) | Second admin, GDPR formalisation, monitoring stack |
| Member onboarding guide | Deck (optional — only if tasks are a real pain today) |

## Infra recipe
- **Hetzner CAX21** (4 vCPU ARM / 8 GB / 80 GB), **billed monthly ~€6.49**. Resizes to the
  production CAX31 in minutes later (disk preserved).
- **Real production domain** (EU registrar, ~£12/yr) — *not* DuckDNS/Tailscale.
- **AIO + Caddy**, public, automatic **Let's Encrypt TLS**. Enable Nextcloud + Talk +
  Collabora. **Skip HPB.**
- **Basic hardening** (it's internet-facing, and this carries forward): keys-only SSH,
  firewall (80/443/22 only), fail2ban, strong admin password, keep AIO updated.
- **BorgBase free tier** (<10 GB free) configured day one. Stash the Borg key in a password
  manager now; formalise into the Proton Pass shared vault when the full org joins.

## Setup steps (~half a day)
1. Register the production domain; point A/AAAA at the box's public IP.
2. Provision CAX21 (verify Collabora has an arm64 image — INFRA-1).
3. Install AIO + Caddy; obtain TLS; enable Nextcloud + Talk + Collabora.
4. Apply basic hardening.
5. Configure BorgBackup → BorgBase; take a first successful backup; save the key.
6. Create 2–5 accounts; seed a shared folder, a calendar, 2–3 Talk channels, a wiki page.
7. Onboard each pilot user (below) and start the friction log.

## Onboarding non-technical pilot users
Use the member onboarding guide (DOC-5). Each user:
- Opens `https://<domain>` / installs the **Nextcloud** + **Talk** apps and logs in.
- Sets up **calendar sync** — iOS native CalDAV, Android via **DAVx5**. *This is the #1
  friction point; capture every snag with screenshots for the guide.*
- Installs the desktop sync client (optional).

## What to measure (friction log)
- Onboarding time per user; where they got stuck (expect: calendar).
- Whether daily org chat actually moves to Talk.
- Group/1:1 call quality without HPB.
- Admin time spent on support and upkeep.

## Growth path to production (no rebuild — same instance)
1. **Resize CAX21 → CAX31** in the Hetzner console (stop, resize, start; disk preserved).
2. **Enable Talk HPB** for reliable group video; add the rest of the members.
3. **Complete the launch blockers before the full org onboards** (they protect production
   data at scale, so they shift here, not before the pilot):
   - Proton Pass vault populated (SEC-2)
   - Restore runbook written + **test-restored** (BKP-4, DOC-2)
   - Backup-failure alerting live (BKP-3)
4. Add monitoring (MON-1), GDPR basics (GOV-3), and recruit the second admin (GOV-7).
5. Backfill the Ansible playbook (ADR-0001) so the now-production box is reproducible.

> Same domain, same data, same AIO instance throughout → members' apps keep working; there
> is no migration, only growth.

## Cost
- CAX21 for 2 months ≈ **€13** (~£11–13 incl. VAT)
- Domain ≈ **£12/yr** *(production spend, not throwaway)*
- BorgBase ≈ **£0** (free tier)
- **Pilot-only cost ≈ ~£13** (the smaller box for two months); everything else carries forward.

## Decision gate (end of pilot)
Review against the three questions, then choose:
- **Proceed** → execute the growth path above (this *is* the start of production).
- **Adjust** → e.g. if group video is poor, plan HPB/Jitsi (COLLAB-6 / ADR-0003); if
  adoption stalls, revisit onboarding or the managed-Nextcloud option (ADR-0010).
- **Stop** → tear down the box (billing stops); domain + learnings retained.
