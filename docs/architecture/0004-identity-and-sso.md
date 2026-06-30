# ADR-0004: Identity — per-app accounts, SSO deferred

- **Status:** Accepted
- **Date:** 2026-06-18
- **Deciders:** Technical admin

## Context
Every service uses per-user accounts (no shared logins). The open question was whether to
unify them behind single sign-on via an Identity Provider (Authentik or Keycloak) using
OIDC.

OIDC/SSO means running one IdP that all apps delegate login to — one account, one login
everywhere, and central deprovisioning (one off-switch when a volunteer leaves). But the
IdP is itself a **fourth stateful, security-critical service** and a **single point of
failure**: if it goes down, *nobody* can log into *anything*. At 5–30 users the only
strong benefit — central deprovisioning — is something the admin can do by hand for 2–3
accounts in a couple of minutes.

Authentik would be the choice over Keycloak if we did this (lighter, ~Python, friendlier
than Keycloak's JVM/~1 GB footprint), but adding *any* IdP to a bus-factor-1 org makes the
single point of failure worse, not better.

## Decision
**Defer SSO.** Use per-user accounts created directly in each service. Revisit only when
(a) a second admin exists, or (b) user churn makes manual deprovisioning genuinely painful.

## Alternatives considered
- **Authentik SSO from the start:** rejected — adds a critical-path service and bus-factor
  risk for marginal benefit at this size.
- **Keycloak:** rejected — heavier than Authentik; same objection, more so.

## Consequences
- **Positive:** no extra service; no new single point of failure; less to back up and patch.
- **Negative / accepted:** members maintain a separate login per service (Nextcloud is the
  main one at launch, so this is minor today). Deprovisioning a departing member is a manual
  checklist rather than one switch — acceptable at this scale and documented in the runbook.
- Note: Matrix's native OIDC (via MAS) was a point in Matrix's favour; with Matrix deferred
  ([0002](0002-chat-layer.md)), that argument is also deferred.

## Conditions / follow-ups
- Reconsider alongside any Phase 2 Matrix work — if Matrix lands, an IdP (Authentik) +
  Matrix's native OIDC may become worthwhile, but only with a second admin in place.
