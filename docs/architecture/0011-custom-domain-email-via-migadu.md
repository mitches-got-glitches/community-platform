# ADR-0011: Custom-domain email via Migadu

- **Status:** Accepted
- **Date:** 2026-07-26
- **Deciders:** Technical admin

## Context
[ADR-0008](0008-operational-baseline.md) decided Nextcloud's own *transactional* mail
(password resets, share notifications, calendar invites) goes through a cheap EU relay
(Scaleway TEM / Mailjet). That is not the same problem as this one: the org now wants real
human mailboxes at `@bafz.org` (e.g. `mitch@bafz.org`) for people to read and send mail —
day-to-day correspondence, not automated system mail. ADR-0008 explicitly scoped itself to
Nextcloud's automated sending only, so this is a new decision, not an extension of it.

Self-hosting a full mail server (Postfix/Dovecot on the VPS) carries the same objection
ADR-0008 already raised against self-hosted outbound mail — deliverability reputation,
SPF/DKIM/DMARC, blocklists — and adds a second bus-factor-1 skill burden (mail server
administration) on top of everything else. It is rejected for the same reason, more so.

The org already registers `bafz.org` as its production domain (Nextcloud lives there too,
per `docs/pilot-plan.md`), and the sovereignty-first ethos rules out US mailbox providers.

## Decision
Host `@bafz.org` mailboxes on **Migadu** (Switzerland): flat-fee, unlimited mailboxes and
aliases per domain, so adding admins or committee members costs nothing extra per seat.
Start on the **Micro** tier (~$19/yr) — plenty for the handful of addresses needed now —
and upgrade tiers only if sending volume or storage needs grow.

**DNS coexists in the same zone, on different record types:**
- Nextcloud's web app keeps its existing A/AAAA (or CNAME) records on its subdomain
  (e.g. `cloud.bafz.org`) — untouched by this decision.
- The `bafz.org` apex gets MX + SPF + DKIM + DMARC records pointing at Migadu.
- **The SPF record must be a single combined TXT record** listing both authorized
  senders — Migadu's `include:` *and* the ADR-0008 transactional relay's `include:`.
  Two separate SPF TXT records for the same domain is invalid per RFC 7208 and breaks
  deliverability for both senders; whoever edits the zone must merge them into one.

Pass/SimpleLogin aliases (Pass Family, [ADR-0007](0007-secrets-management.md)) can mint
`@bafz.org` alias addresses that forward into a Migadu mailbox once the domain is verified
— useful for giving vendor sign-ups or role addresses (e.g. `vault-owner@bafz.org`) a
`bafz.org` identity without creating another real mailbox.

## Alternatives considered
- **Proton Mail Family bundle** (Mail+Pass+Drive+VPN, 6 users, up to 3 custom domains,
  ~£170–200/yr): would let the same Proton account hold both the Pass vault and real
  mailboxes, but alone consumes most of the org's £230–280/yr budget ceiling. Rejected on
  cost — the org would be paying for Drive/VPN/Calendar capacity it doesn't need to solve
  an email-hosting problem.
- **mailbox.org** (Germany): comparable EU alternative, similar cheap-tier pricing. Kept
  as the fallback if Migadu's support or deliverability disappoints — not chosen only
  because there's no reason yet to run two candidates in parallel.
- **Self-hosted mail server:** rejected — same deliverability/maintenance argument as
  ADR-0008, worse (a mail server has a harder reputation/blocklist problem than an
  outbound-only relay).

## Consequences
- **Positive:** real `@bafz.org` addresses for admins/members at flat low cost; unlimited
  mailboxes means growth (per [ADR-0005]'s 20–30 person sizing) costs nothing extra;
  Migadu is off-box, so it is unaffected by a VPS disaster — no mail-hosting step is
  needed in the [restore runbook](../runbooks/restore.md), only DNS re-pointing if the
  *domain* itself were ever compromised.
- **Negative / accepted:** a new vendor dependency and a second mail-related credential
  set (distinct from the ADR-0008 relay) to keep in the Proton Pass vault. The combined-SPF
  requirement is a sharp edge — get it wrong and either transactional mail or human mail
  silently loses deliverability.

## Conditions / follow-ups
- Register/verify the `bafz.org` MX + SPF + DKIM + DMARC records with Migadu; confirm the
  combined SPF record also still passes the ADR-0008 relay's own alignment check.
- Store the Migadu account login (and any mailbox-level app passwords) in the **BAFZ Vault**
  Proton Pass shared vault ([ADR-0007]).
- Add this line item to the cost summary in `CLAUDE.md` and `docs/risks.md` (~£15/yr at
  the Micro tier).
- `docs/architecture/README.md` index needs a row for this ADR.
