# ADR-0009: Bus-factor mitigation and second-admin policy

- **Status:** Accepted
- **Date:** 2026-06-18
- **Deciders:** Technical admin

## Context
The org is run by **one technically capable admin. Bus factor is currently 1**, and there
is **no second admin yet** — the "train a second person" mitigation is, as of this
decision, aspirational. We chose to **self-host everything** (DIY-all) for cost and
sovereignty, which makes the whole continuity story rest on mitigations that must actually
be put in place, not merely planned.

We considered buying down the risk with managed services instead of a person. "Managed"
splits into three archetypes:
- **A. Full DIY VPS** (chosen) — cheapest, max sovereignty/IaC, *worst* bus factor.
- **B. Managed-ops on our own VPS** (etke.cc-style) — keeps data ownership + IaC, vendor
  provides operational continuity; costs money. Best balance for bus factor.
- **C. Fully managed SaaS** (e.g. IONOS managed Nextcloud) — lowest burden, weakest IaC/
  sovereignty; managed *Matrix* alone tends to break the budget.

The budget was also reframed during planning: the original £100–150/yr was unachievable
once off-site backups and a domain were counted. Working ceiling is now **~£250–300/yr**,
with target spend **~£160–180/yr** — leaving slack to fund managed-ops later if needed.

## Decision
**Launch solo, recruit a second admin in parallel, with a hard 3-month target.** Accept a
single-admin window at launch *only because* the following mitigations are in place, which
together mean the system is recoverable by *someone else* even before that someone is
trained:

**Launch blockers (no production data until all true):**
1. **Proton Pass vault populated** — VPS root/SSH, registrar, Borg key, SMTP creds
   ([0007](0007-secrets-management.md)). Credentials survive the admin even before a second
   admin exists.
2. **Restore runbook written and test-restored** against a fresh box
   ([0006](0006-backups-and-disaster-recovery.md)).
3. **Backup-failure alerting live** ([0008](0008-operational-baseline.md)).

**Post-launch obligation:**
- **Second admin onboarded within 3 months of go-live** — given vault access and walked
  through an actual restore. If a second volunteer proves genuinely unrealistic by then,
  **reopen this ADR and adopt archetype B (managed-ops)** for operational continuity rather
  than leaving bus factor at 1 indefinitely.

## Alternatives considered
- **Managed-ops (B) from the start:** rejected for launch on cost, but is the explicit
  fallback if recruiting fails.
- **Fully managed SaaS (C):** rejected — weakest sovereignty/IaC and managed Matrix breaks
  budget.
- **Leave bus factor at 1 with no deadline:** rejected — highest residual risk; the whole
  DIY/sovereignty story is fiction without a real second person or a paid operator.

## Consequences
- **Positive:** complexity was deliberately minimised across the stack (Talk over Matrix,
  no SSO, AIO over hand-rolled) precisely to make single-admin operation and successor
  hand-off realistic.
- **Negative / accepted:** a real single-point-of-failure *window* at launch. The launch
  blockers convert "the admin is gone" from catastrophic to a recoverable rebuild.

## Conditions / follow-ups
- Track the 3-month second-admin deadline explicitly. Re-evaluate DIY-vs-managed-ops at
  that checkpoint.
- **Archetype C (fully managed Nextcloud) is being actively reconsidered** in light of the
  volunteer-time cost finding — see [ADR-0010](0010-diy-vs-managed-nextcloud.md). It carries
  the verification checklist that gates any switch and serves as the concrete fallback if
  the second admin (GOV-7) never materialises.
