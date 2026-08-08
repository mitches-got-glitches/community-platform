# Community talk: personal privacy with Proton Pass

*A planning doc for the committee/speaker — not the slides themselves.*

## Why this talk, why Pass

We already run a Proton Pass shared vault (BAFZ Vault) for our own infrastructure secrets
— see [ADR-0007](architecture/0007-secrets-management.md). This talk turns that into
something members get personal value from too: a practical, non-abstract intro to
protecting *their own* privacy, using a tool we already trust and can demo live rather
than describe secondhand.

Scope is **Pass only** — not the wider Proton suite (Mail/Drive/VPN/Calendar). Keeping it
narrow means the talk stays focused, doubles as a live demo of something the org already
runs, and keeps the pooling ask (below) cheap and simple to organise.

## Talk outline

1. **The problem, made concrete, not abstract.** Not "privacy matters" in the abstract —
   specific, relatable scenarios: reused passwords mean one breached site compromises
   every account that shares the password; giving your real email to every sign-up form
   lets breaches and data brokers link everything back to you and to each other.
2. **Live demo: Proton Pass as a password manager.** Generating strong unique passwords,
   autofill, syncing across devices. The unglamorous but highest-impact habit change.
3. **Live demo: email aliases (built on SimpleLogin).** The idea that lands best: a
   unique alias per sign-up. If spam starts arriving on one alias, you know exactly which
   site leaked or sold it, and you can kill that one alias without touching anything else.
   This is the concrete, memorable "aha" of the talk — plan the most time here.
4. **How to actually start.** Install the app, import existing passwords (most password
   managers/browsers export a CSV Pass can import), pick 3–5 accounts to convert first
   rather than trying to do everything at once.
5. **The cost angle, and the pooling offer** (see process below). A Pass Family plan
   covers 6 people for roughly the price of one person's individual plan — mention that
   BAFZ can introduce members who want to split one, without BAFZ running or paying for
   it themselves.

## Splitting a Pass Family plan: introductions only

BAFZ facilitates members finding each other to split the cost of a Pass Family plan (up
to 6 people). **BAFZ does not collect payment, run the subscription, or hold the vault for
any group that forms this way** — this is a deliberate scope limit, not an oversight: it
keeps BAFZ out of handling other people's money and out of disputes if a group's
arrangement goes wrong later. This is unrelated to and separate from BAFZ's own
infrastructure vault (BAFZ Vault) — a member's personal pooled plan is entirely their own
group's business.

**The process, kept deliberately light:**

1. **Express interest.** After the talk (or any time), interested members tell the
   organiser they'd like to split a Pass Family plan. A simple sign-up sheet or a channel
   in the community space is enough — no form/tooling to build.
2. **Matching.** Whenever there are enough interested people (up to 6 per group), the
   organiser introduces them to each other — an email thread or a group chat is enough.
   No fixed schedule is needed; do this opportunistically after a talk or when interest
   reaches a workable group size.
3. **Handoff, then step back.** Once introduced, the group decides among themselves: who
   owns the Proton account the subscription runs on, how the cost is split and collected,
   and who has authority to remove a member later. BAFZ's role ends at the introduction.
4. **Say the disclaimer out loud, every time.** When making an introduction, state plainly
   that BAFZ isn't a party to whatever the group agrees, doesn't guarantee anyone will pay
   their share, and isn't the one to resolve a dispute if the arrangement breaks down.
   Said once clearly up front avoids an awkward "I thought BAFZ was handling this" later.
5. **Departures are the group's problem, not BAFZ's** — but worth passing on the same
   guidance BAFZ follows for its own vault: if someone leaves the group, remove their
   access and, if they held the login credentials at any point, rotate the account
   password. Whoever owns the group's Proton account should keep that in mind before
   agreeing to be the owner.

## Future expansion: Proton Unlimited / full-suite topics (not yet detailed)

Placeholder list to revisit — this talk currently scopes to Pass only (see "Why this
talk, why Pass" above); these are candidate topics if/when the talk expands to cover the
wider Proton Unlimited bundle. Not fleshed out yet, just captured so the idea isn't lost:

- **Proton Mail** — encrypted email, custom-domain angle (nice tie-in/contrast with our
  own Migadu decision, [ADR-0011](architecture/0011-custom-domain-email-via-migadu.md) —
  worth being clear in the talk about *why* we chose differently for our own org).
- **Proton Calendar** — encrypted calendar, alternative to Google Calendar.
- **Proton Drive** — encrypted file storage, comparison to Google Drive/Dropbox.
- **Proton VPN** — public wifi protection, what a VPN does and doesn't protect against
  (don't oversell it — a common source of privacy-talk snake oil).
- **Proton Wallet** — Bitcoin wallet integration; probably a niche/optional topic.
- **Proton Sentinel** — the higher-tier account-protection program, relevant mainly to
  higher-risk members (activists, journalists, etc. in the community).
- **Dark-web/breach monitoring** — surfacing when an alias or address shows up in a
  known breach.
- **Plan-tier comparison for households** — Unlimited vs Family vs Duo vs individual
  products, cost-per-person breakdown for a household deciding what to subscribe to.
- **Jurisdiction/trust story across the whole suite** — Switzerland as the common thread
  tying all the above together, not just Pass.

## References
- [ADR-0007: Secrets management](architecture/0007-secrets-management.md) — BAFZ's own
  Pass Family setup, the model this talk demos live.
- [Pass Family admin-onboarding runbook](runbooks/pass-family-admin-onboarding.md) — same
  underlying mechanics (share a vault, set access levels) a member group would use, if
  useful to point a curious group at.
