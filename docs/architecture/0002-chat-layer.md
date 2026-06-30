# ADR-0002: Chat — Nextcloud Talk now, Matrix later (managed)

- **Status:** Accepted
- **Date:** 2026-06-18
- **Deciders:** Technical admin

## Context
Required chat features are: channels, channel membership, replies, and **threads**.
The choice was between:

- **Nextcloud Talk** — already in the backbone box (zero extra services). As of Hub 25
  it supports threads, so it meets **all four required features**.
- **Matrix homeserver + Element** — richer: Spaces, power levels, federation, native
  OIDC SSO, and bridges to WhatsApp/Signal/Telegram. Everything Matrix adds is *above*
  the requirements line, i.e. not required.

The org currently has many members on WhatsApp, which makes a **WhatsApp bridge**
(`mautrix-whatsapp`) the one genuinely attractive Matrix feature. But a bridge is also
the single most maintenance-hostile component available:

- It links to WhatsApp's multi-device API like WhatsApp Web — **against WhatsApp's ToS**;
  Meta periodically bans linked-device/bridge sessions, after which the bridge silently
  dies until someone notices and re-links.
- It is a *third* fragile service (homeserver + bridge) to run, patch, and babysit, and
  it breaks whenever WhatsApp changes protocol — the component most likely to page the
  admin at 11pm.
- It **mirrors, it does not migrate** — members stay on WhatsApp; the Matrix room merely
  sees the traffic.

Running this on a bus-factor-1 org is the wrong risk. Crucially, Matrix is also the
component that forces a 16 GB box and roughly doubles ongoing maintenance (see
[0005](0005-hosting-provider-and-sizing.md)).

## Decision
Launch on **Nextcloud Talk** — one stack, in the box, lowest bus factor, meets all
required features. **Defer Matrix + the WhatsApp bridge to Phase 2**, and when added, run
it as **managed Matrix** (etke.cc-style operations on our own VPS, preserving data
ownership and IaC) rather than self-hosting it. Phase 2 is gated on (a) a concrete,
sustained need that Talk can't meet, and (b) a second admin existing.

## Alternatives considered
- **Matrix from day one, DIY:** rejected — maximises maintenance and bus-factor exposure
  for capability we don't yet require.
- **Matrix from day one, managed:** viable but premature — pays a recurring fee and adds
  user-facing complexity before we've confirmed Talk is insufficient.
- **Drop the WhatsApp-mirror idea entirely:** kept as a live option — if Talk meets needs,
  the main reason for Matrix evaporates.

## Consequences
- **Positive:** simplest possible launch; no extra services, RAM, or attack surface;
  consistent with the ARM box sizing and the single-admin reality.
- **Negative / accepted:** no WhatsApp bridging at launch — members on WhatsApp keep using
  it separately. We treat moving the *org's* business into Talk as the goal, not mirroring
  casual WhatsApp chatter. Spaces/federation/power-levels are unavailable; judged
  gold-plating at 5–30 users.
- Phase 2 cost (managed Matrix) is a future line item, funded from budget slack.

## Conditions / follow-ups
- Revisit when: a real need for WhatsApp/Signal bridging is sustained, OR federation with
  another org becomes concrete, AND a second admin is in place.
- If reopened, prefer managed-ops Matrix over self-hosting — see
  [0009](0009-bus-factor-and-second-admin.md).
