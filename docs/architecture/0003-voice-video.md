# ADR-0003: Voice/video — Nextcloud Talk + High Performance Backend

- **Status:** Accepted
- **Date:** 2026-06-18
- **Deciders:** Technical admin

## Context
Voice/video is a required feature. The original options were Jitsi Meet (pragmatic,
~1hr to deploy, separate service) or Element Call (Matrix-native, needs a LiveKit SFU +
MatrixRTC auth service). The chat decision ([0002](0002-chat-layer.md)) removed Matrix
from the launch, which makes **Element Call moot** — it would mean standing up Matrix
purely for calls.

Nextcloud Talk includes voice/video natively: peer-to-peer for small calls, and a
**High Performance Backend (HPB)** — an SFU — for reliable group calls. AIO can deploy
the HPB as part of the same stack, so it adds **no new external service** to operate.

## Decision
Use **Nextcloud Talk's built-in calling with the High Performance Backend** enabled for
group calls at our 20–30 person sizing target. Do **not** pre-emptively deploy Jitsi.

## Alternatives considered
- **Element Call:** rejected — requires Matrix + LiveKit; contradicts [0002].
- **Jitsi from the start:** rejected as premature — a separate service to patch and
  monitor, for capability Talk likely already provides. Kept as a documented fallback.

## Consequences
- **Positive:** one stack; consistent identity (calls use the same Nextcloud accounts);
  no extra attack surface or maintenance.
- **Negative / accepted:** if Talk's group-call quality disappoints at realistic size, we
  add Jitsi later (a ~1hr deploy). We accept a possible later addition rather than paying
  for it speculatively now.
- HPB does increase CPU/bandwidth use during group calls; the chosen box has headroom and
  Hetzner bandwidth (~20 TB) is effectively free — see [0005](0005-hosting-provider-and-sizing.md).

## Update (2026-08-08) — video decoupled; HPB deferred
Two facts revise this ADR (see [`options-paper-2026-08.md`](../options-paper-2026-08.md)):
- **Real group calls are ≤10 people, sometimes with external guests** — within plain Talk's range, so the **High Performance Backend is not required** and is **deferred** (it was sized for 20–30). External guests join Talk conversations via **public/guest links**, no account needed.
- **Voice/video is decoupled from the collaboration host.** Removing HPB as a requirement on the provider is a key reason **managed Nextcloud** becomes viable — see [ADR-0012](0012-diy-vs-managed-nextcloud.md).

**Revised decision:** use **Talk's built-in calling (no HPB)** for the ≤10 case; keep **Jitsi as the documented fallback** if quality disappoints or calls grow. For sovereignty a fallback Jitsi should be **self-hosted on an EU VPS** (~4 GB) — the public **meet.jit.si is operated by 8x8 (US)**, accepted as a **casual/non-sensitive bridge for now** but not for the sovereign stack. Re-enable HPB (DIY) or add Jitsi if calls routinely exceed ~10 (ties to the 50–100 scale scenario and [ADR-0004](0004-identity-and-sso.md)).

## Conditions / follow-ups
- **Pilot test:** a real **10-person Talk call + an external guest** is a success criterion in the [managed-Nextcloud pilot runbook](../runbooks/managed-nextcloud-pilot.md).
- If quality is inadequate at ≤10, deploy a **self-hosted EU Jitsi** as the sidecar and document it.
