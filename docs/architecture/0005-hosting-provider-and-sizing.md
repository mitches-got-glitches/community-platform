# ADR-0005: Hosting — Hetzner CAX31 (ARM), sized for 20–30 users

- **Status:** Accepted
- **Date:** 2026-06-18
- **Deciders:** Technical admin

## Context
We need a cloud VPS (not on-prem) on an EU-owned provider for sovereignty, sized for a
current 5–10 people but with headroom for growth to ~20–30. Key sizing insight: for
Nextcloud + Talk, **user count is not the dominant cost driver** — storage and concurrent
activity are, and the harder wall is **RAM**, driven by how many *services* co-reside on
the box (Nextcloud + Collabora office + Talk HPB, plus anything added later). Going
10 → 30 users is roughly one tier bump + more backup storage; Hetzner bandwidth (~20 TB)
is effectively free, so video calls don't spike the bill.

A second insight: **Hetzner's ARM (Ampere) line is dramatically better value than x86**
for the same RAM, and Nextcloud AIO + Collabora + Talk HPB all run on arm64.

## Decision
**Hetzner CAX31 — 8 vCPU (Ampere ARM) / 16 GB RAM / 160 GB NVMe, ~€14/mo (~£145/yr)**,
located in the EU (Falkenstein/Nuremberg DE or Helsinki FI).

The 16 GB gives real headroom for 20–30 users with collaborative office editing and group
video, while leaving budget for backups. The x86 equivalent (CPX41, 8 vCPU/16 GB) is
~€30/mo (~£300/yr) — double the cost for the same RAM.

## Alternatives considered
- **Hetzner x86 (CPX31/CPX41):** fallback only — chosen if a required AIO add-on lacks an
  arm64 image. CPX31 (4 vCPU/8 GB, ~€16/mo) accepts tighter RAM; CPX41 doubles cost.
- **OVHcloud / Scaleway / IONOS (EU):** viable EU alternatives; Hetzner wins on value.
- **Mythic Beasts (UK residency):** excellent ethical UK-owned host with strong support,
  but **~3–4× the cost for half the cores** — VPS 16 (16 GB / **4** cores) ≈ £48/mo ≈
  **£576/yr (+~20% UK VAT, non-reclaimable)** vs CAX31 (16 GB / **8** ARM cores) ≈
  **£175/yr VAT-incl**. VPS 16 alone breaks the £250–300 ceiling before backups/domain.
  Its UK-soil advantage only upgrades a requirement we've already met (EU residency is
  acceptable under UK–EU adequacy; Hetzner is EU-owned, no US CLOUD Act exposure).
  **Reserve as the UK-residency fallback** if a funder/regulator mandates UK soil or
  reliance on EU adequacy becomes unacceptable.
- **Managed middle path (managed Nextcloud + managed Matrix):** rejected for launch — see
  [0009](0009-bus-factor-and-second-admin.md); managed Matrix alone tends to break budget.

## Consequences
- **Positive:** best price/RAM; EU residency and EU-owned vendor (no US CLOUD Act exposure);
  vertical resize in minutes if we grow.
- **Negative / accepted:** ARM means we must confirm arm64 images for everything we enable.
  Single box = single point of failure for *availability* (mitigated by backups + a fast
  rebuild playbook, not by HA — HA is out of scope at this budget).

## Cost risks (VAT and growth)
The headline ~£145/yr is **ex-VAT**. Real cost is higher and can drift:
- **VAT:** Hetzner adds ~19% German VAT (~£30/yr), **not reclaimable** as we're not
  VAT-registered. This applies to the VPS and any volumes.
- **Storage growth (the sleeper):** the 160 GB on the box covers documents easily, but a
  community org accumulates event photos/media fast. Exceeding it means a Hetzner volume
  (~£0.04/GB/mo → 100 GB ≈ £45/yr) or a bigger box (CAX41/32 GB ≈ £290/yr).
- **FX:** billed in EUR against a GBP budget → exchange drift + ~2–3% card fees.
- **Resize trigger:** if 20–30 users push CPU/RAM, a tier bump is quick but recurring.

See `../risks.md` (risks R-08, R-10) for the consolidated cost picture. The realistic
VAT-inclusive run-rate for the whole stack is ~£230–280/yr, not ~£160–180.

## Conditions / follow-ups
- ✅ **arm64 images verified (2026-06-30).** Every enabled AIO add-on publishes a multi-arch
  `latest` (amd64 + arm64) on Docker Hub: `aio-nextcloud`, `aio-apache`, `aio-collabora`,
  `aio-talk` (HPB/signaling), `aio-talk-recording`, `aio-imaginary`, `aio-fulltextsearch`,
  `aio-clamav`, `aio-whiteboard`. The one historic gap — `aio-talk-recording` was x86-only on
  aarch64 because Selenium lacked arm64 drivers ([AIO issue #5973](https://github.com/nextcloud/all-in-one/issues/5973),
  [discussion #6262](https://github.com/nextcloud/all-in-one/discussions/6262)) — was
  fixed upstream in 2025; arm64 recording images now ship. **CAX31 (ARM) confirmed; the CPX31
  fallback is not required.** Recording remains the most fragile add-on on ARM — re-check it
  first if a future AIO release regresses; the x86 fallback stands if so.
- Sizing assumes Talk-only (no Matrix). Adding Matrix + bridge + an IdP later would push
  RAM use up and is part of why those are deferred — see [0002], [0004].
- Monitor file-store usage; set an alert before the box disk fills.
