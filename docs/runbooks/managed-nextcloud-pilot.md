# Runbook: managed Nextcloud pilot (IONOS £1/mo trial)

**Goal:** cheaply prove whether a managed Nextcloud can be our launch platform — *before* committing real data or migrating off Google/WhatsApp. The pilot answers two questions: **(1) does the managed plan actually deliver our required features** (wiki, tasks, office, files, calendar, ≤10-person calls with guests), and **(2) will members actually use it**.

**Why IONOS first:** the 1 TB / 10-user tier is **£1/mo for 3 months** (then £9/mo), with a **30-day money-back guarantee** — so the trial costs ~£3–9 total and carries near-zero commercial risk. But IONOS is **flagged** (community reports: curated app list, possibly no Collectives/Deck, no `occ`, flaky Collabora), so this pilot is explicitly a **test of whether IONOS is good enough** — not a foregone choice. If it fails the app-freedom gate below, **stop, claim the refund, and pilot [The Good Cloud](https://thegood.cloud/) or [Hetzner Storage Share](https://www.hetzner.com/storage/storage-share/) instead** (both more likely to allow full apps).

See [ADR-0012](../architecture/0012-diy-vs-managed-nextcloud.md) for the decision context and [`options-paper-2026-08.md`](../options-paper-2026-08.md) for the full provider comparison.

## Before you start — two safety rules
- **Use only test data.** Do **not** load real member PII into a throwaway pilot instance (UK GDPR). Use your own account plus 2–3 consenting volunteers and dummy/non-sensitive content. Anything created here may be discarded.
- **Keep the pilot isolated from `bafz.org`'s live mail.** Use the **IONOS-provided default hostname** for the pilot — do **not** repoint `bafz.org` DNS/MX (Proton Mail is live there; the Migadu migration is a separate, later job — see [ADR-0011](../architecture/0011-custom-domain-email-via-migadu.md) and issue #58). Map `cloud.bafz.org` only *after* the pilot graduates to production.

## Step 1 — Sign up
1. Order **IONOS Managed Nextcloud Hosting → 1 TB / 10-user tier** (the £1/mo × 3 promo).
2. Add the **Collabora "Nextcloud Office" add-on** (~£2/mo) so office editing is testable.
3. Record the admin login, URL, and billing/renewal date in the **BAFZ Vault** (Proton Pass, [ADR-0007](../architecture/0007-secrets-management.md)) and note the **30-day refund deadline**.

## Step 2 — The app-freedom gate (make-or-break — do this first)
Before investing any effort, log in as admin and **try to install [Collectives](https://apps.nextcloud.com/apps/collectives) (wiki) and [Deck](https://apps.nextcloud.com/apps/deck) (tasks)** from the app store.
- ✅ **Both install and open** → continue to Step 3.
- ❌ **Either is blocked / not on the allowed list** → IONOS fails two required features. **Stop, claim the money-back, and restart this runbook on The Good Cloud or Hetzner Storage Share.**

## Step 3 — Set up the pilot instance
1. Create the admin account; set a strong password (in the vault).
2. Create **3–5 test users** (you + volunteers; dummy identities, no real PII).
3. Enable/confirm the apps under test: **Files, Talk, Calendar, Contacts, Collectives, Deck, Collabora (Office)**.

## Step 4 — Run the feature checklist (the success criteria)
Tick each against real use, not just "it loads":
- [ ] **Wiki (Collectives):** create a collective, a few linked pages.
- [ ] **Tasks (Deck):** a board with lists + cards, assigned to test users.
- [ ] **Office (Collabora):** create and **co-edit a `.docx` and an `.odt` in the browser** with a second user — does it actually work, and is it fast enough?
- [ ] **Files:** upload, share internally, and share via a **public link** (password-optional).
- [ ] **Calendar:** create events; subscribe from a phone via **CalDAV**; confirm it syncs.
- [ ] **Talk — the video test:** a **10-person call** *and* an **external guest joining via public link**. Judge quality at your real group size.
- [ ] **Notifications:** does the instance send share/notification emails? (Tests SMTP — note whether IONOS handles it or it needs config; ports 25/465/587 are sometimes blocked.)
- [ ] **Performance:** navigation is snappy, not the multi-second lag some users report.

## Step 5 — Prove the exit hedge (portability insurance)
Managed gives no full export ([ADR-0006](../architecture/0006-backups-and-disaster-recovery.md)), so confirm you can always get your data out:
- [ ] Install the **desktop sync client** and confirm it pulls **all files** to a local machine (this is also your off-site backup).
- [ ] **Export a calendar** (`.ics`) and a **Deck board** (JSON) and re-import them somewhere, to prove per-app portability.

## Step 6 — Real-use trial (2–4 weeks)
Have the volunteers use it for one genuine, **non-sensitive** org task (e.g. plan an event in Deck + a Collectives page + a call). Adoption is the real test — features passing on paper isn't enough.

## Step 7 — Decision review
Against Steps 2–6:
- **Pass** → managed launch confirmed. Plan production: pick the final provider/tier, map `cloud.bafz.org`, do the real user onboarding (DOC-4/5), and sequence the Google/WhatsApp move (see `../pilot-plan.md`). Promote [ADR-0012](../architecture/0012-diy-vs-managed-nextcloud.md) to Accepted with the chosen provider.
- **Fail** (esp. Collectives/Deck/Collabora/perf) → refund, and either pilot the next shortlist provider or fall back to the DIY-on-Netcup plan (Decision 1/2 of the options paper).

## Cost
~£1/mo × 3 + ~£2/mo Collabora ≈ **£9 for a 3-month pilot** (or less with the 30-day refund). Trivial next to what it de-risks.
