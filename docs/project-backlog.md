# Project backlog — Community Org Collaboration Stack

Build/launch backlog for the stack decided in [`docs/architecture/`](architecture/).
Structured so it can migrate to **GitHub Issues + Projects** with minimal rework.

## How this maps to GitHub Projects

- **Each `###` task = one GitHub Issue.** Title after the ID becomes the issue title; the
  body (description + acceptance criteria) becomes the issue body.
- **Epics (`##` sections) = a parent "Epic" issue** (or a `Project` group / `epic:` label).
  Link children to the epic issue.
- **The metadata line** maps to GitHub **Project fields**:
  `Labels` → labels · `Milestone` → milestone · `Size` → a Size field · `Priority` → a
  Priority/Status field · `Depends on` → a "Blocked by" relation (or note in body).
- **Acceptance criteria (`- [ ]`)** render as GitHub task-list checkboxes natively.
- Migration tip: this file can be split per-issue and created with
  `gh issue create --title … --body … --label … --milestone …`, or pasted into the
  Project board.

### Label legend
`type:epic` `type:task` `type:runbook` `type:docs` `type:spike`
`area:infra` `area:nextcloud` `area:backups` `area:security` `area:collab` `area:monitoring` `area:onboarding` `area:governance`
`prio:launch-blocker` `prio:p1` `prio:p2` `prio:backlog`
`size:S` `size:M` `size:L`
`pilot` — in scope for the Phase 0 carry-forward pilot (see [`pilot-plan.md`](pilot-plan.md))

### Milestones
- **M0 — Prerequisites & approval** (budget, domain, accounts)
- **M1 — Build** (infra → Nextcloud → backups, behind closed doors)
- **M2 — Launch blockers** (the three non-negotiables; gate to go-live)
- **M3 — Member rollout** (staged migration off WhatsApp/Google)
- **M4 — Post-launch** (second admin, reviews)
- **Backlog — Phase 2** (Matrix, SSO, Jitsi — deferred by ADRs)

### Launch-blocker tasks (must all be ✅ before M3 / production data)
`SEC-2` (vault populated) · `BKP-3` (backup alerting) · `BKP-4` (tested restore) — see
[ADR-0009](architecture/0009-bus-factor-and-second-admin.md). For a carry-forward pilot these
shift to *before the full org onboards*, not before the pilot (see `pilot-plan.md`).

### Phase 0 — Carry-forward pilot (`pilot`)
A cheap 2–5 user / 1–2 month pilot run as a *smaller production instance* (CAX21 + real
domain + public TLS), grown into production by resizing — no rebuild. Full plan in
[`pilot-plan.md`](pilot-plan.md). **Pilot-scope tasks** (tagged `pilot`, with pilot variations):
`INFRA-1` (verify Collabora arm64) · `GOV-2` (register the **production** domain now) ·
`INFRA-4` (basic hardening — public-facing) · `NC-1` (AIO **manually**, no Ansible yet) ·
`NC-4` (a couple of accounts/groups) · `BKP-1` (BorgBase from day one) ·
`COLLAB-1` (files) · `COLLAB-2` (wiki) · `COLLAB-4` (calendar/CalDAV — test hardest) ·
`COLLAB-5` (Talk channels, **no HPB**) · `DOC-5` (onboarding guide).
Everything else (HPB, Ansible, vault, tested restore, alerting, monitoring, 2nd admin, GDPR)
is deferred to the growth path.

---

## Epic A — Foundation & Infrastructure
`type:epic` `area:infra` — *Provision the box and the reproducible base it sits on.*
Refs: [ADR-0001](architecture/0001-nextcloud-backbone-and-deployment.md),
[ADR-0005](architecture/0005-hosting-provider-and-sizing.md),
[ADR-0008](architecture/0008-operational-baseline.md).

### INFRA-1 — Verify arm64 image availability (gating spike)
`type:spike` `area:infra` `prio:launch-blocker` `size:S` `pilot` · **Milestone:** M1 · **ADR:** 0005

Confirm arm64 (Ampere) images exist for every AIO add-on we intend to enable, before
committing to the ARM host. If a critical one is x86-only, the host decision falls back to
Hetzner CPX31.

**Acceptance criteria**
- [ ] arm64 availability confirmed for: Nextcloud AIO core, Collabora, Talk HPB, recording.
- [ ] Decision recorded: proceed on CAX31 (ARM) **or** fall back to CPX31 (x86), with reason.
- [ ] If fallback, ADR-0005 updated and cost summary in CLAUDE.md revised.

### INFRA-2 — Provision the VPS
`type:task` `area:infra` `prio:p1` `size:S` · **Milestone:** M1 · **Depends on:** INFRA-1, M0-2 · **ADR:** 0005

Create the Hetzner CAX31 (or CPX31 fallback) in an EU region (DE/FI), SSH key only.

**Acceptance criteria**
- [ ] VPS running in an EU datacentre; region recorded.
- [ ] Root login is SSH-key only (no password auth).
- [ ] VPS credentials/SSH key recorded in the Proton Pass vault (see SEC-2).
- [ ] A/AAAA DNS records point the org domain/subdomains at the box.

### INFRA-3 — Ansible repo skeleton + inventory
`type:task` `area:infra` `prio:p1` `size:M` · **Milestone:** M1 · **ADR:** 0001

Stand up the git repo structure for the playbook (inventory, group_vars, roles, secrets
handling via vault references, README). This is the IaC spine.

**Acceptance criteria**
- [ ] Repo runs `ansible-playbook --check` cleanly against the host.
- [ ] No plaintext secrets in the repo (references to the vault / Ansible Vault only).
- [ ] README documents prerequisites and the one-command run.

### INFRA-4 — Host hardening role
`type:task` `area:infra` `area:security` `prio:p1` `size:M` `pilot` · **Milestone:** M1 · **ADR:** 0008

Ansible role: `unattended-upgrades`, keys-only SSH, UFW (allow 80/443/SSH only), fail2ban.

**Acceptance criteria**
- [ ] Automatic OS security updates enabled and verified.
- [ ] SSH password auth disabled; firewall denies all but 80/443/SSH.
- [ ] fail2ban active on SSH.
- [ ] Re-running the role is idempotent (no changes on second run).

### INFRA-5 — Docker + Caddy reverse proxy role
`type:task` `area:infra` `prio:p1` `size:M` · **Milestone:** M1 · **ADR:** 0001

Install Docker engine and deploy Caddy with automatic TLS in front of AIO.

**Acceptance criteria**
- [ ] Docker installed and enabled at boot.
- [ ] Caddy serves valid Let's Encrypt TLS for the org domain (A+ on SSL test).
- [ ] Caddy config is version-controlled in the repo.

---

## Epic B — Nextcloud Core
`type:epic` `area:nextcloud` — *Deploy and configure the backbone.*
Ref: [ADR-0001](architecture/0001-nextcloud-backbone-and-deployment.md), [ADR-0008](architecture/0008-operational-baseline.md).

### NC-1 — Deploy Nextcloud AIO via Ansible
`type:task` `area:nextcloud` `prio:p1` `size:L` `pilot` · **Milestone:** M1 · **Depends on:** INFRA-5 · **ADR:** 0001

Playbook drops the AIO `docker-compose.yml` + `.env`, brings up the master container, and
completes initial AIO setup with the required containers enabled (Collabora, Talk + HPB).

**Acceptance criteria**
- [ ] Nextcloud reachable over HTTPS at the org domain.
- [ ] Collabora (office) and Talk HPB containers enabled and healthy.
- [ ] `docker-compose.yml` and `.env` (secrets referenced, not inlined) committed.
- [ ] AIO admin can run an update from the UI successfully.

### NC-2 — Configure outbound SMTP relay
`type:task` `area:nextcloud` `prio:launch-blocker` `size:S` · **Milestone:** M1 · **ADR:** 0008

Point Nextcloud at an EU transactional SMTP relay so password resets, share notifications,
and calendar invites send. (Blocks the email-based user onboarding flow.)

**Acceptance criteria**
- [ ] Test email from Nextcloud arrives (not in spam).
- [ ] SPF/DKIM aligned for the sending domain.
- [ ] Relay credentials stored in the Proton Pass vault.

### NC-3 — Branding & dashboard defaults
`type:task` `area:nextcloud` `prio:p2` `size:S` · **Milestone:** M1

Theming app: org name, logo, colours; sensible default apps and a welcome/dashboard layout.

**Acceptance criteria**
- [ ] Login and dashboard show org branding.
- [ ] New users land on a usable default dashboard.

### NC-4 — Groups & access model
`type:task` `area:nextcloud` `area:security` `prio:p1` `size:S` `pilot` · **Milestone:** M1 · **ADR:** 0004

Create groups (e.g. `committee`, `members`) used for folder/wiki/Talk access. Per-user
accounts, no shared logins, no SSO.

**Acceptance criteria**
- [ ] Groups created and documented.
- [ ] A test member account sees only what its group allows.

### NC-5 — Reproducibility / rebuild test
`type:task` `area:nextcloud` `area:infra` `prio:p1` `size:M` · **Milestone:** M1 · **Depends on:** NC-1 · **ADR:** 0001

Prove the ~95% IaC claim: rebuild a working instance on a fresh VPS from the playbook with
one command (data restored separately via BKP-4).

**Acceptance criteria**
- [ ] Fresh VPS → working Nextcloud via a single documented command.
- [ ] Any manual/UI-only steps are captured in the provisioning runbook (DOC-1).

---

## Epic C — Backups & Disaster Recovery
`type:epic` `area:backups` — *The real continuity story for a bus-factor-1 org.*
Ref: [ADR-0006](architecture/0006-backups-and-disaster-recovery.md), [ADR-0008](architecture/0008-operational-baseline.md).

### BKP-1 — Configure AIO BorgBackup → BorgBase
`type:task` `area:backups` `prio:p1` `size:M` `pilot` · **Milestone:** M1 · **Depends on:** NC-1, SEC-1 · **ADR:** 0006

Point AIO's built-in Borg at a BorgBase repo (EU, free tier). Generate the encryption key.

**Acceptance criteria**
- [ ] A successful backup archive exists in BorgBase.
- [ ] The Borg encryption key is stored in the Proton Pass vault (see SEC-2) — **not** only on the box.
- [ ] Daily automated schedule confirmed running.

### BKP-2 — Retention / prune policy
`type:task` `area:backups` `prio:p2` `size:S` · **Milestone:** M1 · **Depends on:** BKP-1 · **ADR:** 0006

Set prune (e.g. 7 daily / 4 weekly / 6 monthly) so history doesn't outgrow the free tier.

**Acceptance criteria**
- [ ] Prune policy configured and documented.
- [ ] Repo size projected to stay under the 10 GB free tier (or upgrade decision recorded).

### BKP-3 — Backup-failure alerting *(launch blocker)*
`type:task` `area:backups` `area:monitoring` `prio:launch-blocker` `size:S` · **Milestone:** M2 · **Depends on:** BKP-1 · **ADR:** 0008

Healthchecks.io ping on the Borg cron; alert if a backup is missed. Silent failure is the
classic disaster.

**Acceptance criteria**
- [ ] A successful run pings Healthchecks; dashboard shows green.
- [ ] A deliberately failed/skipped run triggers an alert to the admin within the grace period.
- [ ] Healthchecks credentials in the vault.

### BKP-4 — Test restore to a fresh box *(launch blocker)*
`type:task` `area:backups` `prio:launch-blocker` `size:M` · **Milestone:** M2 · **Depends on:** BKP-1, NC-5 · **ADR:** 0006

Restore the latest archive onto a clean VPS and verify data integrity. Produces DOC-2.

**Acceptance criteria**
- [ ] Files, calendar, wiki pages, and Talk history verified present after restore.
- [ ] Restore performed using only the runbook + vault (no undocumented knowledge).
- [ ] Time-to-restore recorded.
- [ ] DOC-2 (restore runbook) validated by this exercise.

### BKP-5 — Quarterly cold export procedure
`type:task` `area:backups` `prio:p2` `size:S` · **Milestone:** M4 · **ADR:** 0006

Establish the 3-2-1 third leg: a manual offline export the admin downloads quarterly.

**Acceptance criteria**
- [ ] First cold export produced and stored off-site/offline.
- [ ] Procedure documented in DOC-3; recurring reminder set.

---

## Epic D — Secrets & Access
`type:epic` `area:security` — *Credentials survive the admin.*
Ref: [ADR-0007](architecture/0007-secrets-management.md).

### SEC-1 — Set up Proton Pass shared vault
`type:task` `area:security` `prio:p1` `size:S` · **Milestone:** M0 · **ADR:** 0007

Create the infrastructure-secrets vault; verify current free-tier sharing limits, upgrade
to a paid plan if needed for multi-admin sharing.

**Acceptance criteria**
- [ ] Shared vault exists and can be shared with a second person.
- [ ] Plan/sharing-limit decision recorded.

### SEC-2 — Populate the vault *(launch blocker)*
`type:task` `area:security` `prio:launch-blocker` `size:S` · **Milestone:** M2 · **Depends on:** SEC-1 · **ADR:** 0007

Store VPS root/SSH, registrar, Borg key, SMTP relay creds, Healthchecks creds.

**Acceptance criteria**
- [ ] All listed credentials present in the vault.
- [ ] Verified that a fresh login to the vault can reach every secret.
- [ ] Vault is *not* hosted on the org's own infrastructure (off-box) — principle check.

---

## Epic E — Collaboration Features
`type:epic` `area:collab` — *Turn the backbone into the things members use.*
Ref: [ADR-0002](architecture/0002-chat-layer.md), [ADR-0003](architecture/0003-voice-video.md).

### COLLAB-1 — Files & shared folder structure
`type:task` `area:collab` `prio:p1` `size:S` `pilot` · **Milestone:** M1 · **Depends on:** NC-4

Create the org folder layout and group permissions; enable desktop/mobile sync.

**Acceptance criteria**
- [ ] Agreed folder structure created with correct group access.
- [ ] Desktop client and mobile app both sync a test file.

### COLLAB-2 — Collectives wiki
`type:task` `area:collab` `prio:p1` `size:S` `pilot` · **Milestone:** M1

Enable Collectives; create the org knowledge base; seed starter pages (about, how-tos,
the member onboarding guide DOC-5).

**Acceptance criteria**
- [ ] A collective exists, owned by a group (not an individual).
- [ ] Two users can co-edit a page; version history works.
- [ ] Starter pages created.

### COLLAB-3 — Deck task board
`type:task` `area:collab` `prio:p2` `size:S` · **Milestone:** M1

Set up the shared task board(s) and access.

**Acceptance criteria**
- [ ] Board created with columns and shared to the right group.
- [ ] A card can be created/assigned/moved by a test member.

### COLLAB-4 — Calendar & CalDAV sync
`type:task` `area:collab` `prio:p1` `size:M` `pilot` · **Milestone:** M1

Create shared calendar(s); verify CalDAV sync end-to-end on both platforms (the fiddliest
onboarding step).

**Acceptance criteria**
- [ ] Shared calendar created and shared to the group.
- [ ] Verified sync on **iOS** (native CalDAV) and **Android** (DAVx5).
- [ ] Steps captured for DOC-5 with screenshots.

### COLLAB-5 — Talk channels & threads
`type:task` `area:collab` `prio:p1` `size:S` `pilot` · **Milestone:** M1 · **ADR:** 0002

Create channels (per topic/committee/event); verify membership, replies, threads.

**Acceptance criteria**
- [ ] Channels created with correct membership.
- [ ] Replies and threads work on web and mobile Talk apps.
- [ ] Push notifications received on mobile.

### COLLAB-6 — Group-call quality test (Jitsi decision gate)
`type:spike` `area:collab` `prio:p1` `size:S` · **Milestone:** M3 · **Depends on:** NC-1 · **ADR:** 0003

Trial Talk + HPB group calls at realistic participant counts; decide whether Jitsi is needed.

**Acceptance criteria**
- [ ] Group call tested at ~target size; quality assessed.
- [ ] Decision recorded: HPB sufficient **or** raise PHASE2-3 (deploy Jitsi).

---

## Epic F — Monitoring & Operations
`type:epic` `area:monitoring` — Ref: [ADR-0008](architecture/0008-operational-baseline.md).

### MON-1 — External uptime monitor
`type:task` `area:monitoring` `prio:p1` `size:S` · **Milestone:** M2

A monitor *external to the box* that alerts when the site is unreachable.

**Acceptance criteria**
- [ ] Uptime check on the org URL with alerting to the admin.
- [ ] Verified alert fires on a simulated outage.

### MON-2 — Update cadence definition
`type:docs` `area:monitoring` `prio:p2` `size:S` · **Milestone:** M4

Define and document the cadence for AIO updates and host patching (links DOC-6).

**Acceptance criteria**
- [ ] Cadence agreed (e.g. monthly AIO update window) and documented in DOC-6.

---

## Epic G — Runbooks & Documentation
`type:epic` `area:onboarding` — *The bus-factor insurance. Each item is a deliverable doc.*
Ref: [ADR-0009](architecture/0009-bus-factor-and-second-admin.md).

### DOC-1 — Provisioning / rebuild-from-scratch runbook
`type:runbook` `area:infra` `prio:p1` `size:M` · **Milestone:** M1 · **Depends on:** NC-5

Step-by-step to rebuild the whole stack on a bare VPS from the playbook, incl. any UI-only steps.

**Acceptance criteria**
- [ ] A second person can follow it to stand up a working instance unaided.
- [ ] Covers every manual step not captured in code.

### DOC-2 — Disaster-recovery restore runbook
`type:runbook` `area:backups` `prio:launch-blocker` `size:M` · **Milestone:** M2 · **Depends on:** BKP-4

Restore data from BorgBase onto a fresh instance, using only the vault + this doc.

**Acceptance criteria**
- [ ] Validated by the BKP-4 test restore (someone other than the author can follow it).
- [ ] Includes where the Borg key lives and how to retrieve it from the vault.

### DOC-3 — Backup verification runbook
`type:runbook` `area:backups` `prio:p2` `size:S` · **Milestone:** M4 · **Depends on:** BKP-5

How to run the quarterly restore spot-check and cold export.

**Acceptance criteria**
- [ ] Procedure + schedule documented; first run completed.

### DOC-4 — User provisioning (admin) runbook
`type:runbook` `area:onboarding` `prio:p1` `size:S` · **Milestone:** M3 · **Depends on:** NC-2, NC-4

How an admin creates/configures a new member account and adds them to groups.

**Acceptance criteria**
- [ ] Covers account creation, group assignment, quota, welcome email.
- [ ] A non-author admin successfully provisions a test user from it.

### DOC-5 — Member onboarding guide (user-facing)
`type:docs` `area:onboarding` `prio:p1` `size:M` `pilot` · **Milestone:** M3 · **Depends on:** COLLAB-4, COLLAB-5

The one-page guide promised in the proposal: set password, install apps, join channels,
**set up calendar (iOS + Android/DAVx5 with screenshots)**.

**Acceptance criteria**
- [ ] A new member can self-onboard from the guide with no help for the common path.
- [ ] Calendar/CalDAV section has platform-specific screenshots.
- [ ] Published in the wiki (Collectives).

### DOC-6 — Update / upgrade runbook
`type:runbook` `area:infra` `prio:p2` `size:S` · **Milestone:** M4 · **Depends on:** MON-2

How to apply AIO updates and host patches safely, and roll back if needed.

**Acceptance criteria**
- [ ] Covers AIO update flow, host updates, pre-update backup check, rollback.

### DOC-7 — Incident / outage runbook
`type:runbook` `area:monitoring` `prio:p2` `size:S` · **Milestone:** M4

First-response checklist when the box/site is down (what to check, escalation).

**Acceptance criteria**
- [ ] Triage steps from "alert received" to "service restored or escalated".

### DOC-8 — Member offboarding runbook
`type:runbook` `area:security` `prio:p2` `size:S` · **Milestone:** M3 · **Depends on:** NC-4 · **ADR:** 0004

Manual deprovision (no SSO): disable account, reassign owned data, revoke shares.

**Acceptance criteria**
- [ ] Checklist ensures a departing member loses all access and leaves no orphaned data.

### DOC-9 — Secrets / vault management runbook
`type:runbook` `area:security` `prio:p2` `size:S` · **Milestone:** M3 · **Depends on:** SEC-2

How the vault is structured, who has access, and how to rotate a credential.

**Acceptance criteria**
- [ ] Documents vault layout, access list, and a credential-rotation procedure.

---

## Epic H — Launch & Governance
`type:epic` `area:governance`

### GOV-1 — Committee approves proposal + budget
`type:task` `area:governance` `prio:p1` `size:S` · **Milestone:** M0

Present `docs/proposal-for-the-org.md`; secure ~£180/yr budget and the staged-move mandate.

**Acceptance criteria**
- [ ] Budget approved and minuted.
- [ ] Mandate to proceed with staged migration recorded.

### GOV-2 — Register domain (EU registrar)
`type:task` `area:governance` `area:infra` `prio:p1` `size:S` `pilot` · **Milestone:** M0 · **ADR:** 0005

Register/transfer the org domain with an EU registrar; store creds in the vault.

**Acceptance criteria**
- [ ] Domain registered with an EU registrar; auto-renew on.
- [ ] Registrar credentials in the Proton Pass vault.

### GOV-3 — UK GDPR baseline
`type:task` `area:governance` `prio:p1` `size:M` · **Milestone:** M3

As data controller: a short privacy notice, lawful basis, a data inventory, and a basic
breach-response note.

**Acceptance criteria**
- [ ] Privacy notice published to members.
- [ ] Data inventory (what we hold, where, retention) recorded.
- [ ] Breach-response steps documented.

### GOV-4 — Launch-blocker gate check
`type:task` `area:governance` `prio:launch-blocker` `size:S` · **Milestone:** M2 · **Depends on:** SEC-2, BKP-3, BKP-4

Verify all three launch blockers are complete before any production data / member rollout.

**Acceptance criteria**
- [ ] SEC-2, BKP-3, BKP-4 all ✅ and evidenced.
- [ ] Go/no-go decision recorded.

### GOV-5 — Pilot with a small group
`type:task` `area:governance` `prio:p1` `size:M` · **Milestone:** M3 · **Depends on:** GOV-4, DOC-5

Onboard 2–3 friendly members; gather friction points before full rollout.

**Acceptance criteria**
- [ ] Pilot users onboarded via DOC-5; feedback captured as issues.

### GOV-6 — Staged member rollout
`type:task` `area:governance` `prio:p1` `size:L` · **Milestone:** M3 · **Depends on:** GOV-5

Move foundations first (files/calendar/wiki), then chat channel-by-channel; keep WhatsApp
for casual during transition.

**Acceptance criteria**
- [ ] All members have accounts and have completed onboarding.
- [ ] Org business is happening in Talk channels; key files/calendar/wiki migrated off Google.

### GOV-7 — Recruit & onboard second admin (≤3 months)
`type:task` `area:governance` `prio:p1` `size:M` · **Milestone:** M4 · **Depends on:** GOV-6 · **ADR:** 0009

The standing bus-factor obligation. Hard 3-month target from go-live.

**Acceptance criteria**
- [ ] Second admin identified, given vault access, and walked through an actual restore (DOC-2).
- [ ] If unmet by the deadline: ADR-0009 reopened and managed-ops fallback evaluated.

### GOV-8 — One-month review
`type:task` `area:governance` `prio:p2` `size:S` · **Milestone:** M4 · **Depends on:** GOV-6

Review adoption and pain points; resolve COLLAB-6 (Jitsi?) and any deferred decisions.

**Acceptance criteria**
- [ ] Review held; actions logged; Jitsi decision finalised.

---

## Backlog — Phase 2 (deferred by ADRs)
`type:epic` `prio:backlog`

### PHASE2-1 — Evaluate Matrix + WhatsApp bridge (managed)
`prio:backlog` `area:collab` · **ADR:** 0002 — Gated on a sustained need Talk can't meet **and** a second admin. Prefer managed-ops, not self-hosted.

### PHASE2-2 — Evaluate SSO (Authentik)
`prio:backlog` `area:security` · **ADR:** 0004 — Reconsider when a second admin exists or churn makes manual deprovisioning painful.

### PHASE2-3 — Deploy Jitsi (if Talk video inadequate)
`prio:backlog` `area:collab` · **ADR:** 0003 — Raised only if COLLAB-6 finds HPB insufficient.
