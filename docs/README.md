# Documentation map

This repo's docs follow [Diátaxis](https://diataxis.fr/): four types, each answering a
different question, distinguished by whether the reader is **studying** or **working**,
and whether they need **practical** or **theoretical** knowledge.

| Type | Answers | Form | Where it lives here |
|---|---|---|---|
| **Tutorial** | "Can you teach me to…?" | A lesson — learning-oriented | *(none yet — see below)* |
| **How-to guide** | "How do I…?" | A series of steps — goal-oriented | [`runbooks/`](runbooks/), [`ONBOARDING.md`](../ONBOARDING.md) |
| **Reference** | "What is…?" | Dry description — information-oriented | [`reference/`](reference/) *(added as written)* |
| **Explanation** | "Why…?" | Discursive — understanding-oriented | [`architecture/`](architecture/) (the ADRs) |

Existing folder names predate this mapping and aren't renamed to match — `architecture/`
and `runbooks/` are themselves well-understood terms (ADR, runbook) that happen to sit
squarely in the *explanation* and *how-to* quadrants respectively. New docs go through the
same classification even though the folder names don't spell it out.

## Applying this to new docs

Before writing, pick **one** quadrant — don't mix modes in a single doc:
- Explaining a decision and its trade-offs → **explanation** (`architecture/`, a new ADR).
- Walking through a specific operational task start-to-finish → **how-to** (`runbooks/`).
- Listing facts with no narrative (a vault layout, a port map, an app/group inventory) →
  **reference** (`reference/` — create it when the first reference doc is written).
- Teaching a newcomer a skill by doing it, optimised for a first-time success rather than
  completeness → **tutorial**. Nothing here yet; the natural first candidate is **DOC-5**
  (member onboarding guide) — reserve `docs/tutorials/` for it rather than folding it into
  `runbooks/`.

A doc that tries to be two of these at once (e.g. a runbook that stops to explain *why*
at length) is a sign it should split into two docs, cross-linked.

## Out of scope for this map

`docs/guides/` holds cross-cutting conventions for *contributors to this repo*
(e.g. [`commit-conventions.md`](guides/commit-conventions.md)) rather than docs *about the
product* — Diátaxis targets the latter, so house-style/process docs sit outside the four
quadrants deliberately.

Planning docs in this directory (`proposal-for-the-org.md`, `risks.md`, `pilot-plan.md`)
are project/governance artifacts, not documentation for a user of the stack — also
intentionally outside this map. `docs/archive/` is explicitly archived and no longer
maintained (see its banner).
