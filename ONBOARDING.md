# Admin onboarding runbook

This is the hand-off doc for a **second admin** taking shared ownership of the community
org's self-hosted collaboration stack. It exists to kill bus factor 1: by the end of it you
can get into everything, understand how the box is built, and rebuild it from backups.

It is the concrete artifact behind the ADR-0009 post-launch obligation — *second admin
onboarded within 3 months of go-live, given vault access and walked through an actual
restore* (see the [bus-factor ADR](docs/architecture/0009-bus-factor-and-second-admin.md)).

**Audience:** an incoming technically-capable volunteer admin (comfortable on a Linux CLI).

**Last updated:** 2026-06-30

**Owner:** current technical admin (the person handing this to you).

---

## Table of Contents

- [How the stack is built (the 60-second model)](#how-the-stack-is-built-the-60-second-model)
- [Step 0 — get access first](#step-0--get-access-first)
- [The CLI toolchain](#the-cli-toolchain)
- [Where everything lives](#where-everything-lives)
- [Routine operations](#routine-operations)
- [Backups and restore](#backups-and-restore)
- [Monitoring and alerts](#monitoring-and-alerts)
- [Your first-week checklist](#your-first-week-checklist)
- [Where to read next](#where-to-read-next)

---

## How the stack is built (the 60-second model)

One **Hetzner CAX31** VPS (ARM, EU) runs everything. The layers, top to bottom:

- **Caddy** terminates TLS and reverse-proxies to Nextcloud (automatic HTTPS).
- **Nextcloud All-in-One (AIO)** is the application. AIO is itself a "mastercontainer" that
  owns a fleet of child containers (Nextcloud, database, Redis, Collabora office, Talk +
  the High Performance Backend, Borg backup). **You do not hand-manage those containers** —
  AIO does, including safe coordinated upgrades. You drive it from its admin UI.
- **Ansible** is how the *host* gets built: it provisions/holds the box config — Docker,
  the AIO compose + `.env`, the Caddy config, and host hardening (keys-only SSH, UFW,
  `fail2ban`, unattended security upgrades). The playbook lives in git. **A bare VPS + the
  playbook + the Proton Pass secrets = the whole system rebuilt in roughly one command.**

The key mental split: **AIO owns the app and its upgrades; Ansible owns the host and the
edge; git holds both as code.** Full reasoning in the
[deployment ADR](docs/architecture/0001-nextcloud-backbone-and-deployment.md).

What is *not* in git (and so lives only in backups + this runbook): AIO's post-install UI
tweaks and Docker volume state. That gap is exactly why the restore runbook matters.

## Step 0 — get access first

Nothing else works until you can unlock the secrets. The infrastructure credentials live in
a **Proton Pass shared vault**, deliberately off the box it protects (see the
[secrets ADR](docs/architecture/0007-secrets-management.md)).

1. Create a **Proton account** and send the current admin your Proton address.
2. They share the **infra vault** with you. (Heads-up: on the Proton free tier a vault tops
   out at 2 free users — the vault owner is on **Pass Plus** so sharing isn't blocked.)
3. Confirm you can see, at minimum:
   - **VPS root / SSH** access (key or root password) for the Hetzner box.
   - **Hetzner Cloud** console login (to reboot/rebuild/resize the VPS).
   - **Domain registrar** login (DNS records point at the box).
   - **Borg backup key / passphrase** — *the* item that makes backups recoverable by you.
   - **SMTP relay** credentials and **Healthchecks.io** / uptime-monitor logins.
4. Get **read/write access to the IaC git repo** (this repo) — the Ansible playbook and these docs.

If any of those are missing from the vault, that is a launch-blocker regression — flag it to
the current admin before going further.

## The CLI toolchain

Install these on your own machine. None are exotic; most are one package each.

| Tool | What you use it for | Install (macOS / Debian) |
|------|--------------------|--------------------------|
| **`ssh`** + your SSH key | Get onto the box. Key-only — password auth is disabled. | preinstalled |
| **`git`** | Clone the IaC repo (playbook + docs). | `brew install git` / `apt install git` |
| **Ansible** | Run the playbook: build a fresh host, re-apply config, host hardening. | `brew install ansible` / `apt install ansible` |
| **Proton Pass** (app or browser ext) | Unlock the infra vault. | [proton.me/pass](https://proton.me/pass) |
| **`docker` / `docker compose`** | Inspect AIO containers on the box and run `occ`. Used *on the VPS*, not locally. | already on the box |
| **`borg`** (BorgBackup) | Inspect/restore archives, and the quarterly cold export. | `brew install borgbackup` / `apt install borgbackup` |
| **`hcloud`** (Hetzner CLI, optional) | Script VPS create/resize/reboot instead of the web console. | `brew install hcloud` |

You mostly operate the *application* through AIO's web admin UI, not the CLI — the CLI is for
the host, deployments, and restores.

## Where everything lives

| Thing | Where |
|-------|-------|
| Public Nextcloud | `https://<your-domain>` (proxied by Caddy) |
| **AIO admin interface** | `https://<host>:8080` — backups, upgrades, container status, restore |
| IaC (Ansible playbook, configs) | this git repo |
| Infra secrets | Proton Pass shared vault |
| Off-site backups | BorgBase (EU), separate vendor from Hetzner |
| Backup alerting | Healthchecks.io |
| External uptime monitor | (see vault for login) |

Replace `<your-domain>` / `<host>` with the real values from the vault — they're intentionally
not written into this repo.

## Routine operations

- **Run / re-apply the host config:** `ansible-playbook` against the inventory (see the repo
  README). Idempotent — safe to re-run; it reconciles the box to what's in git.
- **Nextcloud admin tasks** (`occ`): exec into the Nextcloud container on the box, e.g.
  `docker exec -it nextcloud-aio-nextcloud occ <command>`.
- **Upgrades:** done from the **AIO admin UI** ("Stop containers" → "Update"). AIO sequences
  the multi-container upgrade safely — this is the whole reason we chose AIO over hand-rolled
  Compose. **Re-test a restore after any major AIO upgrade.**
- **Reboot / resize / rebuild the VPS:** Hetzner Cloud console or `hcloud`.

## Backups and restore

This is the part that actually matters for bus factor — read the
[backups & DR ADR](docs/architecture/0006-backups-and-disaster-recovery.md) in full.

- **Engine:** AIO's built-in **BorgBackup** — consistent DB dump + volume snapshot, encrypted
  with the Borg key.
- **Off-site:** **BorgBase** (EU, different vendor from Hetzner, so genuinely off-site).
- **Third copy:** a **quarterly manual cold export** the admin downloads and stores separately.
- **Key custody:** the Borg key lives in the Proton Pass vault — *that's what lets you, the
  second admin, open the backups at all.* No key = unrecoverable backups.

> **The restore runbook is a separate, step-by-step document** (`docs/runbooks/restore.md`)
> covering the AIO UI-driven rebuild on a fresh box — including the UI tweaks and volume state
> that git doesn't capture. Writing it and **test-restoring it against a fresh box is a launch
> blocker**. If that doc doesn't exist or hasn't been test-restored yet, that's the single most
> important gap to close — your onboarding is not complete until you have personally walked a
> restore.

## Monitoring and alerts

- **Healthchecks.io** pings the Borg backup cron and shouts if a backup is *missed* — a silent
  backup failure is the classic self-hosting disaster, so this must be live before any
  production data.
- An **external uptime monitor** watches the box from outside (on-box monitoring can't tell you
  the box is down).
- Make sure **alerts reach you too**, not just the original admin — that's the whole point of a
  second admin. See the [operational baseline ADR](docs/architecture/0008-operational-baseline.md).

## Your first-week checklist

- [ ] Proton account created; infra vault shared with you; you can read every secret listed in [Step 0](#step-0--get-access-first).
- [ ] You can `ssh` onto the box with your own key.
- [ ] You can log into the Hetzner Cloud console and the domain registrar.
- [ ] You've cloned the IaC repo and read the playbook top to bottom.
- [ ] You can open the AIO admin UI at `:8080` and see container/backup status.
- [ ] You've located the Borg key in the vault and confirmed it opens the BorgBase repo.
- [ ] **You have personally completed a test restore against a fresh box** using the restore runbook.
- [ ] Monitoring/backup alerts are wired to reach you.

When every box is ticked, the org is no longer bus-factor 1.

## Where to read next

- [Architecture decision records](docs/architecture/README.md) — the full set of ADRs; start with
  [0001 (deployment)](docs/architecture/0001-nextcloud-backbone-and-deployment.md),
  [0006 (backups/DR)](docs/architecture/0006-backups-and-disaster-recovery.md), and
  [0009 (bus factor)](docs/architecture/0009-bus-factor-and-second-admin.md).
- [Risks register](docs/risks.md) — the consolidated cost and operational-risk picture.
- `CLAUDE.md` — project overview, hard constraints, launch blockers.
