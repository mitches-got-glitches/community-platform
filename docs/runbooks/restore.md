# Disaster-recovery restore runbook

Restore the whole stack onto a **fresh box** from the off-site BorgBase backup, using only
this document and the Proton Pass vault. This is the artifact behind backlog item **DOC-2**,
validated by **BKP-4**, and the second of the three launch blockers.

It assumes the worst realistic case: **the VPS is gone** (provider outage, account lockout,
catastrophic corruption) and you are rebuilding from nothing. The same steps cover the milder
case of reinstalling AIO on a surviving box.

**Last updated:** 2026-06-30

**Owner:** technical admin

> [!WARNING]
> **This runbook is NOT validated until a test restore (BKP-4) has been walked end-to-end by
> someone other than its author, against a genuinely fresh box.** Until that exercise is done
> and this banner is removed, treat every step as a draft to be corrected *during* the test —
> an untested backup is not a backup. AIO's restore UI wording changes between releases;
> verify labels against the version you are actually restoring.

---

## Table of Contents

- [When to use this](#when-to-use-this)
- [Before you start — what you need](#before-you-start--what-you-need)
- [Retrieve the Borg secrets from the vault](#retrieve-the-borg-secrets-from-the-vault)
- [Restore procedure](#restore-procedure)
- [Verify the restore](#verify-the-restore)
- [Record the outcome](#record-the-outcome)
- [If it goes wrong](#if-it-goes-wrong)
- [After a real restore](#after-a-real-restore)
- [References](#references)

---

## When to use this

- The VPS is destroyed, unreachable, or the Hetzner account is locked out (R-06, R-07).
- A failed AIO upgrade or data corruption needs a roll-back to the last good archive (R-17).
- A scheduled **BKP-4** test restore (run before go-live, and re-run after every major AIO
  upgrade).

For accidental deletion of a *single* file or wiki page, do **not** use this — use Nextcloud's
trash bin and file version history first (R-22). Full restore is the heavy hammer.

## Before you start — what you need

Get all of this in front of you *first*; a restore stalls badly if you discover a missing
credential halfway through.

From the **Proton Pass vault** (see the [secrets ADR](../architecture/0007-secrets-management.md)):

- **Borg repository location** — the BorgBase repo URL (e.g. `ssh://<id>@<id>.repo.borgbase.com/./repo`).
- **Borg encryption key / passphrase** — *the* item without which the archive cannot be opened (R-05).
- **BorgBase SSH key** — the key authorised to read the repo (if separate from the above).
- **Hetzner Cloud** login — to create the replacement VPS.
- **Domain registrar** login — to re-point DNS at the new box.
- **SMTP relay** + **Healthchecks.io** credentials — to restore outbound mail and re-arm alerting.

Also have:

- The **IaC git repo** (this repo) cloned locally — the Ansible playbook rebuilds the host.
- Your **SSH key** for the new box.
- The [provisioning/rebuild runbook (DOC-1)](#references) — this DR runbook restores *data*;
  DOC-1 covers any host/UI build steps not captured in the playbook.

## Retrieve the Borg secrets from the vault

1. Unlock the Proton Pass shared vault (your own Proton login; the vault is shared to you).
2. Copy the **Borg repo URL** and **encryption passphrase** into a scratch note you control —
   you will paste them into the AIO restore screen.
3. If a dedicated BorgBase SSH key is stored as an attachment, save it locally with `600`
   permissions; you will need it for AIO to reach the repo.

> The key lives off the box on purpose: a disaster that destroys the VPS does not destroy the
> means to open its backups. If the key is *not* in the vault, stop — that is a launch-blocker
> regression (SEC-2), and the archive may be unrecoverable.

## Restore procedure

### 1. Provision a fresh box

Create a new Hetzner VPS of the **same type** as production (CAX31, EU region) — match the
architecture so the restored containers run. Key-only SSH.

You can do this from the Hetzner console or, preferably, by running the Ansible playbook's
provisioning against a new host so the box comes up hardened and Docker-ready in one step
(see DOC-1). At minimum the box needs: Docker, the firewall (80/443/SSH), and the AIO
mastercontainer — exactly what the playbook installs.

### 2. Re-point DNS

In the registrar, update the A/AAAA records for the org domain/subdomains to the new box's IP.
DNS propagation can take minutes to hours — start this early so TLS issuance isn't blocked
later. (Lower the TTL in advance if you ever plan a controlled migration.)

### 3. Bring up AIO and choose "restore", not "fresh install"

Open the **AIO admin interface** at `https://<new-host>:8080` and log in with the AIO
passphrase shown on first start.

In the AIO setup flow, choose the **restore from backup** option rather than starting a new
instance. AIO will ask for:

- the **backup/repo location** — paste the BorgBase repo URL;
- the **encryption password** — paste the Borg passphrase from the vault;
- (for a remote repo) it must be able to reach BorgBase over SSH — ensure the authorised key
  is in place.

AIO connects to the Borg repo and lists the available archives.

### 4. Select the archive and restore

- Pick the **most recent good archive** (for a roll-back after a bad upgrade, pick the last
  archive *before* the upgrade).
- Start the restore. AIO pulls the encrypted archive, restores the database dump and all
  container volumes consistently, and re-creates the child containers.
- This is minutes-to-hours depending on data size and network — it is a *rebuild-and-restore*,
  not high availability (R-06, accepted).

### 5. Start the containers and let TLS issue

Start the Nextcloud stack from the AIO UI. Caddy requests a fresh Let's Encrypt certificate for
the domain — this needs the DNS from step 2 to have propagated and ports 80/443 open.

### 6. Re-apply anything not captured in the backup

The Borg archive carries Nextcloud data, config, and volume state. Re-check the items that live
*outside* it:

- **SMTP relay** settings in Nextcloud (re-enter from the vault if needed) — NC-2.
- **Healthchecks.io** ping on the Borg cron — re-arm so the new box's backups are monitored (BKP-3).
- **External uptime monitor** — point it at the restored URL (MON-1).
- Any **AIO UI-only tweaks** documented in DOC-1.

## Verify the restore

Do not declare success until all of these pass (these are the BKP-4 acceptance criteria):

- [ ] Nextcloud loads over **HTTPS** at the org domain with a valid certificate.
- [ ] **Files**: a known test file is present and downloads intact; desktop/mobile client re-syncs.
- [ ] **Calendar**: shared calendar(s) present; a CalDAV client still syncs events.
- [ ] **Wiki**: Collectives pages present with version history.
- [ ] **Talk**: channels and **message history** present.
- [ ] **Login**: an existing member account can log in (auth/data restored, not reset).
- [ ] **Mail**: a Nextcloud test email sends via the relay (password-reset/share path works).
- [ ] **Backups**: the next scheduled Borg run succeeds *from the new box* and pings Healthchecks.

## Record the outcome

Capture these every time this runbook is exercised (real or test):

- **Date** and reason (test / real incident).
- **Time-to-restore** — from "fresh box created" to "all verification boxes ticked". This is
  your real recovery time; the org should know it.
- **Archive restored** (timestamp) and resulting **data-loss window** — how far back the last
  archive was.
- **Any step that was wrong or missing** — fix it in this doc in the same session. That
  correction loop is the entire point of BKP-4.

## If it goes wrong

- **AIO can't reach the Borg repo:** check the BorgBase SSH key is authorised and the repo URL
  is exact; confirm outbound SSH from the box isn't blocked by the firewall.
- **"passphrase incorrect" / can't decrypt:** re-copy the passphrase from the vault (watch for
  trailing whitespace). If it is genuinely wrong, the archive cannot be opened — escalate; this
  is the R-05 nightmare and the reason the key is vaulted and the restore is tested.
- **TLS won't issue:** DNS hasn't propagated, or 80/443 is firewalled — recheck steps 2 and 1.
- **Restore half-completes:** prefer starting clean (rebuild the box) over patching a partial
  restore — a known-clean rebuild beats an ambiguous state.
- Keep the **old/broken box** (if it still exists) untouched until the restore is verified — it
  may hold the only copy of something the archive missed.

## After a real restore

- Rotate any credential that may have been exposed in the incident (VPS root, then update the vault).
- Note the incident, recovery time, and data-loss window against **R-06** in the [risk register](../risks.md).
- If this was post-upgrade recovery, hold off re-attempting the AIO upgrade until you know why
  it failed (DOC-6).

## References

- [Backups & DR ADR (0006)](../architecture/0006-backups-and-disaster-recovery.md) — engine, off-site target, key custody.
- [Secrets ADR (0007)](../architecture/0007-secrets-management.md) — where the Borg key lives.
- [Deployment ADR (0001)](../architecture/0001-nextcloud-backbone-and-deployment.md) — what is/ isn't captured in code.
- [Risk register](../risks.md) — R-04 (unrecoverable backup), R-05 (lost key), R-06 (no HA), R-07 (provider lockout).
- [Project backlog](../project-backlog.md) — DOC-1 (provisioning runbook), BKP-3 (alerting), BKP-4 (the test that validates this doc).
- `ONBOARDING.md` (repo root) — the second-admin hand-off that points here.
