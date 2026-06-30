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

## Conditions / follow-ups
- Trial group calls at realistic participant counts before declaring this closed. If
  quality is inadequate, deploy Jitsi as a sidecar service and document it.
