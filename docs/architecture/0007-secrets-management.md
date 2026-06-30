# ADR-0007: Secrets management — Proton Pass shared vault

- **Status:** Accepted
- **Date:** 2026-06-18
- **Deciders:** Technical admin

## Context
Infrastructure secrets — VPS root/SSH, domain registrar, the **Borg backup key**, SMTP
relay credentials, and any future SSO admin — must be stored so they survive the admin
(bus factor 1) and can be shared with a future second admin. This is *infrastructure*
secret storage, not day-to-day app login (each service has its own accounts — see
[0004](0004-identity-and-sso.md)).

Two non-negotiable principles for *this* use case dominate the brand choice:

1. **The vault must live OFF the infrastructure it protects.** This rules out
   self-hosting Vaultwarden/Bitwarden on the same VPS: a disaster destroys the VPS, but
   you need the credentials *stored on it* to rebuild it — a chicken-and-egg failure. The
   vault must be a hosted, end-to-end-encrypted service independent of our box.
2. **At least two people can unlock it** — otherwise the vault is just another
   bus-factor-1 component.

## Decision
Use a **Proton Pass shared vault** for infrastructure secrets only. It is end-to-end /
zero-knowledge encrypted, Swiss-jurisdiction (strong privacy law, GDPR-adequate, no US
CLOUD Act exposure), supports shared vaults for a future second admin, and aligns with the
org's anti-big-tech, sovereignty-first ethos.

## Alternatives considered
- **Bitwarden (cloud):** excellent team sharing and cheap, zero-knowledge — but **US
  jurisdiction** (CLOUD Act). Confidentiality holds (content encrypted); Switzerland still
  edges it on jurisdiction. Strong runner-up.
- **Vaultwarden (self-hosted):** rejected outright — violates principle 1 (vault on the
  same infrastructure it protects).
- **1Password:** best-in-class UX, but proprietary and US/Canada — off-ethos.
- **KeePassXC shared `.kdbx`:** free and fully sovereign, but multi-admin sync is
  manual/clunky, and storing the file only in Nextcloud re-creates the chicken-and-egg
  problem. Acceptable as an *offline emergency export*, not the primary.

## Consequences
- **Positive:** secrets survive the admin; recoverable by a second admin; sovereign and
  off-box; matches the stack philosophy.
- **Negative / accepted:** dependency on Proton as a vendor. Not a registered nonprofit, so
  no Proton nonprofit discount — but a low-cost paid Pass plan (if needed for vault sharing)
  is a rounding error against budget.

## Conditions / follow-ups
- **Launch blocker:** populate the vault with VPS root, registrar, and Borg key *before*
  any production data — credentials must survive the admin even before a second admin
  exists (see [0009](0009-bus-factor-and-second-admin.md)).
- ✅ **Free-tier sharing limits verified (2026-06-30) — paid plan needed.** Per Proton's own
  docs ([share via extension](https://proton.me/support/pass-browser-share),
  [share on Android](https://proton.me/support/pass-android-share)), **Proton Pass Free** allows
  **2 shared vaults, max 3 people per vault** (including you), and — the binding limit — **at
  most 2 Proton Free users per shared vault**. Any **paid** plan raises this to 50 vaults /
  10 people per vault. Our one infra vault for two *free* admins fits the 3-person cap today,
  but is at the free-user ceiling: a third holder (e.g. a committee backup) is impossible
  until the **vault owner** upgrades. **Decision: put the admin (vault owner) on Pass Plus
  (~£2/mo ≈ £24/yr)** — cheapest acceptable option, removes the headcount cliff, sits at the
  bottom of the budgeted range. This is a hidden cost the original plan treated as £0; budget
  ~£24/yr (not £0); see `../risks.md` (risk R-08).
