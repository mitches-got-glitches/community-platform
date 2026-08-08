# ADR-0012: DIY vs Managed Nextcloud (reconsidering archetype C)

- **Status:** Proposed → leaning **Accept (managed launch)**, gated on the pilot app-freedom test — see the [2026-08-08 update](#update-2026-08-08--providerpricing-gathered-managed-is-the-leaning-launch-path)
- **Date:** 2026-06-18
- **Deciders:** Technical admin
- **Relates to:** [ADR-0001](0001-nextcloud-backbone-and-deployment.md) (deployment),
  [ADR-0009](0009-bus-factor-and-second-admin.md) (archetype C was rejected for launch),
  [`../risks.md`](../risks.md) (R-01 bus factor, R-21 volunteer time, R-08 cost)

## Context
Two things converged to justify reopening the DIY-vs-managed question that ADR-0009
settled on "DIY for launch":

1. **Community consensus on Nextcloud's #1 pain is ops/upgrades.** The recurring
   "Nextcloud sucks" complaints are: resource-heavy, *major upgrades break*, mobile/sync
   flakiness, and "it's a monolith — use best-of-breed apps instead." Our DIY mitigations
   already address most (AIO for safe upgrades, a 16 GB box for performance), and we
   deliberately *reject* the best-of-breed prescription because 5+ services is the wrong
   trade for a bus-factor-1 org.
2. **Our own cost analysis found volunteer time is the largest real cost** — days to build,
   then ~2–5 hrs/month forever — and that bus factor is 1. Managed Nextcloud attacks
   *exactly those two problems*, which is new enough information to revisit archetype C.

"Managed Nextcloud" here means a hosted provider operates the Nextcloud instance for us.
Leading EU/sovereign options: **Hetzner Storage Share** (managed Nextcloud by our existing
trusted EU vendor), **IONOS Managed Nextcloud** (~£9/mo up to 10 users), **hosting.de**.

## Comparison

| Dimension | **DIY VPS (current plan)** | **Managed Nextcloud** |
|-----------|----------------------------|------------------------|
| Cost/yr (indicative) | ~£230–280 VAT-incl. | Comparable–higher: IONOS ~£108/yr (≤10 users); Hetzner Storage Share ~£60–140/yr by storage; scales with users/storage |
| **Volunteer time** | build + **2–5 hrs/mo forever** | **near-zero ops** — provider patches/upgrades/backs up |
| **Bus factor (R-01)** | rests on admin + un-recruited 2nd admin | provider *is* the operational continuity; low successor bar |
| **Upgrade pain (community #1 complaint)** | ours to own (mitigated by AIO) | provider's problem |
| Data sovereignty | ✅ "infra we control" | ⚠️ softens to "EU vendor controls infra" (still EU/GDPR-fine) |
| Code-first / IaC | ✅ ~95% reproducible | ❌ largely click-ops — **breaks a hard constraint** |
| **App freedom (the dealbreaker)** | ✅ Talk + **HPB group video**, Collectives, Deck | ⚠️ **many plans restrict apps** — group-call HPB & Collabora often unavailable |
| Time to launch | days–weeks | hours |
| Exit / portability | full control of data + config | depends on provider export terms |

## The trade in one sentence
Managed Nextcloud buys down our **two biggest problems (bus factor + volunteer time)** for
similar money, at the cost of **two hard constraints (infra control + code-first IaC)** and
a real risk that **group video and some apps aren't available**.

## Decision
**Not decided — do not switch blindly.** The plan of record remains DIY (ADR-0001/0009)
*until* the verification checklist below is answered. Decision rule:

- **If** a sovereign managed provider (preferably Hetzner Storage Share) supports Talk + HPB
  group video, Collectives, and Deck at acceptable cost **→ managed Nextcloud becomes the
  recommended option**, because it fits our *actual* priorities (resilience over control)
  better than DIY. We would then supersede the relevant parts of ADR-0001/0009 and relax
  the "code-first" and "infra we control" constraints deliberately and on the record.
- **If not** (no group video / limited apps) **→ DIY plan stands**, and managed Nextcloud
  remains only the ADR-0009 fallback if the second admin never materialises.

## Consequences
- Keeping this as a live, documented contender means the second-admin deadline (GOV-7)
  has a concrete alternative if recruiting fails — better than scrambling later.
- If we switch, group video may *still* need a separate Jitsi (managed plans rarely host
  the HPB) — fold that into the cost comparison before deciding.

## Update (2026-08-08) — provider/pricing gathered; managed is the leaning launch path
Real research (see [`options-paper-2026-08.md`](../options-paper-2026-08.md)) resolves most of the checklist:

- **The gate moved.** Real group calls are **≤10 with guests**, so **HPB group video is no longer required** ([ADR-0003](0003-voice-video.md) update) — it stops gating provider choice. The **new gate is app freedom**: can the plan install **Collectives (wiki) + Deck (tasks)** and run a working office suite? Those are required features.
- **IONOS is flagged 🚩.** Community reports: **curated app list, no arbitrary installs** (Collectives/Deck likely unavailable), **no OnlyOffice**, **flaky Collabora**, **no `occ`**, plus performance/outdated-version complaints. Marketing disagrees and reports cite old versions → **unverified-but-risky**. Pricing (Managed Nextcloud Hosting): **£1/mo × 3 promo then £9/mo** (1 TB / 10 users); Collabora a ~£2/mo add-on.
- **Shortlist re-ranked to full-Nextcloud managed providers:** **The Good Cloud** (🇳🇱 EU-owned, Nextcloud partner) and **Hetzner Storage Share** (🇩🇪 trusted vendor; its only gap was HPB, now moot). Both need a pre-sales/pilot confirm on Collectives + Deck + office.
- **Cost at ≤10 users favours managed:** ~£108–130/yr vs ~£198/yr for the DIY server, *plus* near-zero ops — the bus-factor win. The curve **inverts by ~25–50 users**; DIY-on-Netcup ([ADR-0010](0010-vps-provisioning-via-opentofu.md)) is the on-trigger target.

**Leaning decision:** **managed Nextcloud for launch**, provider chosen via the [pilot runbook](../runbooks/managed-nextcloud-pilot.md) app-freedom test (IONOS as the cheap first test; The Good Cloud / Hetzner Storage Share if it fails). This **consciously relaxes two `CLAUDE.md` hard constraints for the launch period** — *"infra we control"* → *"an EU vendor controls the box under our account"* (still EU/GDPR-sovereign), and *"code-first IaC"* → largely click-ops — accepted deliberately, on record, as the price of buying down bus factor + volunteer time. It **eases [ADR-0009](0009-bus-factor-and-second-admin.md)**: the provider is operational continuity, so the 2nd-admin deadline is less acute.

**Exit is a planned, triggered move** (managed → DIY-on-Netcup). Managed gives no clean export, so migration is per-app — files via the day-one sync copy, calendars `.ics`, contacts `.vcf`, Deck JSON, Collectives markdown; **Talk history is sacrificed**. **Triggers:** (1) a required feature hits the managed wall; (2) cost inverts with scale (~25–50+ users); (3) a second admin exists and wants IaC control; (4) sovereignty/vendor terms tighten; (5) provider failure. **Hedge:** run the day-one own-copy sync from launch ([ADR-0006](0006-backups-and-disaster-recovery.md) update) — both off-site backup and migration insurance. Switching cost grows with accumulated history, so if DIY is judged inevitable, migrate while data is light.

## Things to check next time (verification checklist)
Answer these before promoting this ADR to Accepted or rejecting it. Carry over to the next
working session.

**App / feature support (the gating questions — answer first):**
- [ ] Does the provider allow enabling **Talk**, and specifically the **High Performance
      Backend** for reliable **group video at 20–30 people**? (Most likely "no" — confirm.)
- [ ] Is **Collectives** (wiki) available/installable?
- [ ] Is **Deck** (tasks) available/installable?
- [ ] Is **Collabora/OnlyOffice** (collaborative office) included, and at what limit?
- [ ] Can we install **arbitrary App Store apps**, or only a curated subset?
- [ ] Is there **`occ` / admin shell** access if we ever need it?

**Cost at our real scale:**
- [ ] Price for **20–30 users** (not just the ≤10 headline tier) — Hetzner Storage Share, IONOS, hosting.de.
- [ ] **Storage pricing** and how it grows (ties to risk R-10 — media/photo growth).
- [ ] Is pricing **VAT-inclusive**? (We can't reclaim VAT — risk R-08.)
- [ ] If group video needs a **separate Jitsi**, add that cost to the managed total.

**Sovereignty & compliance:**
- [ ] Provider's **data location** and legal entity (EU-owned? US parent? CLOUD Act exposure?).
- [ ] **GDPR data-processing agreement (DPA)** available and signable.
- [ ] Encryption at rest; who holds keys.

**Continuity & exit (don't trade one lock-in for another):**
- [ ] **Data export / portability** — can we pull a full Nextcloud export and self-host later?
- [ ] **Backup ownership** — does the provider back up, can we *also* take our own off-site
      copy (preserve the BorgBase off-site principle, R-07)?
- [ ] **SLA / uptime** commitment and support responsiveness.
- [ ] Provider's own viability/track record (avoid R-18 vendor-shutdown risk).

**Migration (if we switch):**
- [ ] Can the provider **import** an existing Nextcloud, or is it a fresh start?
- [ ] How are **per-user accounts** provisioned (affects DOC-4)?

**Decision inputs:**
- [ ] Re-confirm whether a **second admin** is realistically coming (GOV-7) — if yes, DIY's
      bus-factor downside shrinks and the case for managed weakens.
