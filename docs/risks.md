# Risk register — Community Org Collaboration Stack

Living register of the risks in the self-hosted stack, with mitigations cross-referenced
to ADRs (`architecture/`) and backlog tasks (`project-backlog.md`). Includes the realistic
cost picture (the original budget understated several items).

**Owner:** technical admin (until a second admin exists — itself risk R-01).
**Review cadence:** at the one-month review (GOV-8), then quarterly, and after any major
incident or AIO upgrade.

## Scoring
Likelihood × Impact, each Low / Med / High.

| Rating | Meaning |
|--------|---------|
| 🔴 **Critical** | High impact and at least Med likelihood — actively manage; has a hard mitigation/gate. |
| 🟠 **High** | Significant; mitigation required before or shortly after launch. |
| 🟡 **Medium** | Monitor and mitigate pragmatically. |
| 🟢 **Low** | Accept and note. |

---

## Register (sorted by rating)

| ID | Risk | L | I | Rating | Mitigation | Refs |
|----|------|---|---|--------|-----------|------|
| **R-01** | **Bus factor 1** — a single admin builds and runs everything; knowledge/recovery rests on one person. | H | H | 🔴 | Launch blockers (vault, tested restore, alerting); runbooks (DOC-1…9); **2nd admin ≤3 months**; minimise complexity (Talk over Matrix, no SSO). | ADR-0009; GOV-7; DOC-* |
| **R-02** | **Second admin never materialises**, leaving bus factor at 1 indefinitely. | M | H | 🔴 | Hard 3-month deadline; if unmet, **reopen ADR-0009 and adopt managed-ops** (etke-style) as paid operational continuity. | ADR-0009; GOV-7 |
| **R-03** | **Silent backup failure** — backups stop working unnoticed; discovered only when needed. | M | H | 🔴 | Healthchecks.io alert on the Borg cron (loud failure); part of launch gate. | ADR-0006/0008; BKP-3; GOV-4 |
| **R-04** | **Unrecoverable backup** — backups exist but restore was never proven. | M | H | 🔴 | Test restore to a fresh box before go-live; runbook validated by the exercise. | ADR-0006; BKP-4; DOC-2; GOV-4 |
| **R-05** | **Borg key lost / held only by the admin** → off-site backups nobody can open. | M | H | 🔴 | Borg key stored in the off-box Proton Pass vault from day one. | ADR-0006/0007; SEC-2 |
| **R-08** | **Cost overrun / hidden costs** (VAT, vault sharing, storage growth) push spend past budget. | H | M | 🟠 | Realistic VAT-inclusive budget below (~£230–280); monitor storage; Phase 2 = budget conversation. | ADR-0005; cost section ↓ |
| **R-10** | **File-storage growth** exceeds the 160 GB box (event media/photos). | M | M | 🟠 | Alert before disk fills; add a Hetzner volume or resize (quick). Budget £0–80/yr. | ADR-0005; cost section ↓ |
| **R-06** | **Single VPS = no high availability** — hardware/provider outage = downtime. | M | M | 🟠 | Accepted at this budget; fast rebuild-from-code + restore (minutes–hours), not HA. | ADR-0005/0006; DOC-1/2 |
| **R-07** | **Provider account lockout** (Hetzner) could take the box. | L | H | 🟠 | Off-site backup is a **different vendor** (BorgBase); credentials in vault; data portable. | ADR-0006; SEC-2 |
| **R-13** | **Low member adoption** — resistance to leaving WhatsApp/Google. | M | M | 🟠 | Staged rollout; keep WhatsApp for casual; clear onboarding guide + hands-on session; pilot first. | proposal; DOC-5; GOV-5/6 |
| **R-16** | **Security breach** of an exposed, internet-facing stack. | M | H | 🟠 | Host hardening (keys-only SSH, UFW, fail2ban), unattended security updates, TLS, monitoring; secrets off-box. | ADR-0008; INFRA-4; SEC-2 |
| **R-15** | **UK GDPR non-compliance** — we become data controller without the basics in place. | M | M | 🟡 | Privacy notice, lawful basis, data inventory, breach-response note. | GOV-3 |
| **R-17** | **AIO upgrade breaks service.** | M | M | 🟡 | Pre-update backup check; AIO blocks unsafe jumps; update runbook with rollback; re-test restore after majors. | ADR-0001; DOC-6 |
| **R-11** | **ARM image incompatibility** for an AIO add-on. | L | M | 🟡 | Gating spike before host commit; x86 (CPX31) fallback documented. | ADR-0005; INFRA-1 |
| **R-21** | **Volunteer burnout** — ongoing ~2–5 hrs/month support load on one person. | M | M | 🟡 | Realistic expectation-setting; 2nd admin; managed-ops fallback; complexity kept low. | ADR-0009; R-01/R-02 |
| **R-14** | **Calendar/CalDAV onboarding friction** (esp. Android/DAVx5). | H | L | 🟡 | Step-by-step guide with platform screenshots; hands-on session. | DOC-5; COLLAB-4 |
| **R-18** | **Vendor/project dependency** — Nextcloud, BorgBase, or Proton changes terms or shuts down. | L | M | 🟡 | Open formats (Markdown wiki, standard files, Borg, CalDAV) keep data portable; documented exit. | ADR-0001/0006/0007 |
| **R-22** | **User error** — accidental deletion of files/pages. | M | L | 🟢 | Nextcloud trash + file/version history; daily backups. | ADR-0006 |
| **R-23** | **Domain expiry** lapses (missed renewal) → outage + name loss risk. | L | M | 🟢 | Auto-renew on; registrar creds in vault; EU registrar. | GOV-2; ADR-0005 |
| **R-20** | **Payment friction** — personal card pays; expiry/owner-leaving disrupts billing. | M | L | 🟢 | Org payment method or shared billing; billing access in vault. | SEC-2 |
| **R-19** | **Push-notification dependency** on Nextcloud's proxy + Apple/Google gateways. | L | L | 🟢 | Accepted minor sovereignty asterisk; app data still flows only to our server. | ADR-0008 |
| **R-12** | **WhatsApp bridge fragility** (Phase 2 only) — ToS bans, breakage. | M | M | 🟡 *(deferred)* | Deferred entirely; if adopted, **managed Matrix only**, never DIY, and with a 2nd admin. | ADR-0002; PHASE2-1 |

---

## Top risks at a glance
The five 🔴 risks (R-01 to R-05) all reduce to one theme: **a one-person operation must be
recoverable by someone else.** They are precisely why the three **launch blockers** exist
and why GOV-4 gates go-live. If only five things are ever done, do those.

---

## 2026-08 reassessment — managed-launch pivot (pending pilot)
The stack direction shifted materially (see [`options-paper-2026-08.md`](options-paper-2026-08.md)): **Hetzner ARM is unavailable and pricier**, so DIY hosting moves to **Netcup** (on-trigger); **managed Nextcloud is the leaning launch path** (IONOS real-data pilot → likely **The Good Cloud**); **video is decoupled** to Talk-≤10 / Jitsi; and **branch email** goes to Migadu. A full re-score follows once the provider is chosen — key deltas now:

**Eased by a managed launch**
- **R-01 / R-02 / R-21** (bus factor, no 2nd admin, burnout): the provider becomes operational continuity (patches, upgrades, infra), so a solo launch is far less fragile and the 2nd-admin deadline is less acute — [ADR-0012](architecture/0012-diy-vs-managed-nextcloud.md), [ADR-0009](architecture/0009-bus-factor-and-second-admin.md).
- **R-11 / R-17** (ARM images, AIO upgrade breakage): moot on managed; relevant only to the DIY-on-trigger path.

**New or elevated**
- **R-24 (new) 🟠 — managed lock-in / no clean export.** IONOS gives no export/DB/`occ`; migrating real data off is lossy. *Mitigate:* day-one own-copy sync ([ADR-0006](architecture/0006-backups-and-disaster-recovery.md)); prefer a full-Nextcloud provider (The Good Cloud) with proper export.
- **R-25 (new) 🟠 — provider excludes data-loss liability; backup is the customer's job.** IONOS T&Cs cap liability at ~12 months' fees and *"in no circumstances… liable to recover Your data."* Even on managed, our own copy is the sole protection — folds into R-03/R-04.
- **R-26 (new) 🟠 — managed-provider GDPR/processor misuse.** IONOS marketing consent / ad use of data; without a **processor-only DPA** (member-data carve-out, EU storage) we breach controller duties. *Gate:* signed DPA **before** real member data. (relates R-15)
- **R-27 (new) 🟠 — multi-sender email deliverability + Proton→Migadu cutover.** `bafz.org` will carry Migadu + Qomon + relay (+ live Proton); the SPF 10-lookup limit and the MX cutover can break mail. *Mitigate:* one combined SPF, staged migration with rollback — [ADR-0011](architecture/0011-custom-domain-email-via-migadu.md), issue #58.
- **R-28 (new) 🟡 — Qomon dependency.** Member/supporter PII sits in Qomon (SaaS, and a `bafz.org` sender); needs a DPA and a continuity/export note.
- **R-18 (elevated → 🟠) — vendor continuity.** Now spans the managed provider (IONOS can terminate on 30 days, no SLA; The Good Cloud is a small B.V.) plus Migadu and Qomon. Portability + own-copy remain the mitigation.
- **R-15 (elevated → 🟠) — UK GDPR.** Real member data now spans managed Nextcloud + Migadu + Qomon; the **RoPA + DPA register + access/deletion process** (records-to-track, options paper) move from nice-to-have to **required**.
- **Sovereignty constraint consciously relaxed:** managed softens *"infra we control"* to *"an EU vendor controls the box under our account,"* and drops code-first IaC for the launch period — accepted on record ([ADR-0012](architecture/0012-diy-vs-managed-nextcloud.md)).

**⚠️ The cost table below is stale** — it assumes Hetzner CAX31 (unavailable/pricier post-June-2026) and DIY. Re-baseline against the options-paper cost scenarios (managed ~£108–130/yr at ≤10 users; Migadu likely **Mini ~£70**, not Micro) once the provider is chosen.

---

## Cost estimates (the original budget understated this)

The early £100–150/yr was unachievable; the working plan said ~£160–180/yr, but that figure
was **ex-VAT and ignored several items**. The honest run-rate:

| Item | £/yr | Likelihood | Note |
|------|------|------------|------|
| Hetzner CAX31 VPS (ex-VAT) | ~145 | certain | Base compute |
| **VAT on EU services (~19%)** | **30–40** | certain | **Biggest quiet cost; not reclaimable (not VAT-registered)** |
| Proton Pass Family (BAFZ Vault, dedicated org account) | 38–47 | certain | Implemented 2026-07-26 — see [ADR-0007](architecture/0007-secrets-management.md) |
| Custom-domain email (Migadu, `@bafz.org`) | 15–19 | certain | New — see [ADR-0011](architecture/0011-custom-domain-email-via-migadu.md) |
| Off-site backup (BorgBase) | 0–20 | conditional | Free <10 GB; ~£20 at 100 GB |
| File-storage growth | 0–80 | conditional | **Sleeper** — media/photos → volume or bigger box |
| Domain (EU registrar) | 12–15 | certain | Renewal may exceed teaser pricing |
| FX + card fees | 10–15 | certain | EUR/USD billing vs GBP budget |
| SMTP relay / monitoring | ~0 | certain | Free tiers (Scaleway TEM/Mailjet, Healthchecks) |
| **Realistic total** | **~£245–300+** | | Pass Family + Migadu add ~£15–20/yr net over the old Pass Plus line — **now presses the £250–300 ceiling rather than sitting under it**. Worth a deliberate re-check against actual member-storage growth before committing further spend. |

**Genuinely free (not hidden):** Caddy/Let's Encrypt TLS, Collabora CODE, Talk HPB/TURN
bandwidth (within Hetzner's ~20 TB), monitoring free tiers.

### The largest cost isn't in the table: volunteer time
- **Build:** realistically days–weeks of evenings across all epics (not the ~1.5 days that
  is *just* the Nextcloud deploy task).
- **Ongoing:** ~2–5 hrs/month for updates, monitoring, and member support — indefinitely.
- This is "free" only because one volunteer absorbs it, which loops directly back to
  **R-01/R-21**. When that time stops, the £-budget is irrelevant.

### Phase 2 funding gap
The slack we assumed would fund managed Matrix is largely consumed by VAT + Proton +
storage. **Adding Matrix/bridge later is a committee budget-increase conversation, not a
fit within the current envelope** (ADR-0002, PHASE2-1).

### Per-member micro-cost
Android members need **DAVx5** for calendar sync (~£4 once on Play Store, free on F-Droid).
Members usually bear this; noted so it isn't a surprise.
