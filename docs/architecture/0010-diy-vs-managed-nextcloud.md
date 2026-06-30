# ADR-0010: DIY vs Managed Nextcloud (reconsidering archetype C)

- **Status:** Proposed — *pending provider verification (see checklist below)*
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
