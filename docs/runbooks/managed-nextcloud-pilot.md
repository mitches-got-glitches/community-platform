# Runbook: managed Nextcloud pilot (IONOS £1/mo trial)

**Goal:** prove whether a managed Nextcloud can be our launch platform by **running real projects on it**. The pilot answers two questions: **(1) does the managed plan actually deliver our required features** (tasks/projects, wiki, office, files, calendar, ≤10-person calls with guests), and **(2) will members actually use it**. Because we are using **real member data**, treat this as a **soft launch** (see pre-conditions below), not a throwaway test.

**Why IONOS first:** the 1 TB / 10-user tier is **£1/mo for 3 months** (then £9/mo), with a **30-day money-back guarantee** — so the trial costs ~£3–9 total and carries near-zero commercial risk. But IONOS is **flagged** (community reports: curated app list, possibly no Collectives/Deck, no `occ`, flaky Collabora), so this pilot is explicitly a **test of whether IONOS is good enough** — not a foregone choice. If it fails the app-freedom gate below, **stop, claim the refund, and pilot [The Good Cloud](https://thegood.cloud/) or [Hetzner Storage Share](https://www.hetzner.com/storage/storage-share/) instead** (both more likely to allow full apps).

See [ADR-0012](../architecture/0012-diy-vs-managed-nextcloud.md) for the decision context and [`options-paper-2026-08.md`](../options-paper-2026-08.md) for the full provider comparison.

## Pilot mode: real data (soft launch)
This pilot uses **real member data and real projects**, so it is effectively a **soft launch**, not a throwaway test — which raises the stakes, especially on the flagged IONOS. Three **hard pre-conditions before any member data goes in:**
- **A signed processor-only DPA is in place** — the provider acts as *processor*, processing member data **only on our instructions**, with **no marketing/ad use of member or service data**, EU storage, and a sub-processor list (UK GDPR Art 28). **Decline the marketing consent** at signup. Do not load real data until this is confirmed. See [ADR-0012](../architecture/0012-diy-vs-managed-nextcloud.md).
- **The day-one own-copy sync is running** (Step 5, brought forward) — a desktop-sync/`rclone` pull of all files to storage we own, from the moment real data lands. It is our backup *and* our exit insurance ([ADR-0006](../architecture/0006-backups-and-disaster-recovery.md)); the provider's T&Cs disclaim liability for data loss, so this is on us.
- **An exit/deletion plan exists** — how to export our data and have the provider delete it (honouring data-subject requests) if the pilot ends. Real data means real deletion obligations.

> **Reconsider the provider for a real-data pilot.** The £1 IONOS trial made sense as a *throwaway* test. With real data you are launching, and migrating real data *off* IONOS later is lossy (no export). Strongly consider running the real-data pilot on **[The Good Cloud](https://thegood.cloud/)** — the provider you'd actually keep (EU-owned, no ads/tracking, likely full apps) — and reserve IONOS for a quick throwaway app-freedom check only.

**Mailbox stays isolated (agreed):** do **not** touch `bafz.org` **MX/SPF/apex** — Proton Mail stays live and the Migadu migration is a separate later job ([ADR-0011](../architecture/0011-custom-domain-email-via-migadu.md), issue #58).

**Domain for the pilot — note we do *not* currently control `bafz.org`'s DNS** (a separate admin holds it). Options, easiest first:
- **(a) IONOS default hostname** — if offered, zero DNS work and fully isolated; launch today, move to a real domain later.
- **(b) Ask the `bafz.org` admin to add *one* record** — a single `cloud.bafz.org` A/CNAME → the IONOS instance. You don't need to own the domain, just get this added; it **does not touch mail** and gives the right long-term URL.
- **(c) Register a cheap dedicated domain we control** (~£12/yr) for a clean, dependency-free URL.

In every case: **never** change `bafz.org` nameservers or apex `MX`/`SPF`/`DMARC`. Establishing **org control of `bafz.org`** (registrar access in the org's name, in the vault, auto-renew) is a pre-production governance task — see [R-29](../risks.md).

## Step 1 — Sign up
1. Order **IONOS Managed Nextcloud Hosting → 1 TB / 10-user tier** (the £1/mo × 3 promo).
2. Add the **Collabora "Nextcloud Office" add-on** (~£2/mo) so office editing is testable.
3. Record the admin login, URL, and billing/renewal date in the **BAFZ Vault** (Proton Pass, [ADR-0007](../architecture/0007-secrets-management.md)) and note the **30-day refund deadline**.

> **IONOS terms to note (GTC, before real data):** ~~after 30 days you enter a **12-month minimum term**~~ — **corrected 2026-09-22: this contract is rolling monthly.** The GTC's 12-month default reads *"**Unless otherwise specified**, Services are provided for a minimum contract term of 12 months"*, and our contract page **does** otherwise specify: **Contract term: 1 month**. So we are **not** locked in — we can leave at any month boundary, giving **≥1 working day's notice before the renewal date** (GTC Clause 4). The 30-day money-back window (closed ~2026-09-07) was the *refund* route, not the only *exit* route. **Backups are explicitly your responsibility** and IONOS disclaims liability for data loss (*"in no circumstances… liable to recover Your data,"* liability capped at ~12 months' fees) — so the day-one own-copy sync is essential, not optional. **No SLA/uptime guarantee**; IONOS may terminate on **30 days' notice**; and **no guaranteed data export/retrieval on exit**. Obtain and review the **separate DPA** before loading member data. These are standard cheap-managed terms but a poor fit for "the org's resilient home" — [The Good Cloud](https://thegood.cloud/) likely offers better (managed backups included); compare its terms.

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

## Pilot findings (2026-08) — running log
| Check | Result |
|---|---|
| Domain | IONOS default hostname (`nc-…nextcloud-ionos.com`) — isolated from `bafz.org` ✅ |
| Deck (tasks) installs | ✅ |
| Collectives (wiki) installs | ✅ |
| **App-freedom gate** | **PASSED** — contradicts the older community reports |
| Collabora / Office | ✅ **works** — the "Failed to load" was a **Firefox / Privacy Badger** cross-domain block, *not* IONOS (works in Chrome, and in Firefox with Privacy Badger/tracking-protection off for the site). ⚠️ **Onboarding note (DOC-5):** members must allow the Collabora domain / disable tracking protection for the Nextcloud site, or documents won't open. |
| Talk threads (**required feature**) | ✅ **available (re-checked 2026-09-22)** — IONOS moved the instance to **Nextcloud 32 / Hub 25 ("Autumn 25")**, bumping **Talk to v22**, and **threads are enabled**. Supersedes the 2026-08 finding (then on Talk 21.1 / NC 31). **The last required-feature gap on IONOS is closed.** Residual: **the ~1-year lag is real** — Hub 25 "Autumn" shipped upstream in **September 2025**, so IONOS runs roughly **12 months behind**, and upgrade timing is theirs, not ours. **Accepted (2026-09-22):** a ~1-year lag is tolerable *now that every required app is present*; the standing implication is that any **future** required feature should be assumed **~12 months away**, and we plan around that rather than against it. |
| Users / Teams | in progress |
| 10-person call + guest | ⏳ pending |
| Performance | ⏳ pending |
| Day-one backup sync | ⏳ pending |
| DPA + declined marketing consent | ⏳ pending — **required before real member data** |

## Contract dates (recorded 2026-09-22)
| Item | Contract | Active since | Renews on |
|---|---|---|---|
| IONOS Managed Nextcloud 1 TB | 300256038 | 2026-08-08 (Sat) | **2026-10-07 (Wed)** |
| IONOS Collabora Online — 5 Users (add-on) | 300256038 | 2026-08-08 (Sat) | **2026-10-08 (Thu)** |

- **The 30-day money-back window closed ~2026-09-07** — the cheap exit is gone; any exit from here is a cancellation, not a refund.
- **Decision deadline: end of Mon 2026-10-05** (cancellation needs ≥1 working day before the 7 Oct renewal). Diary it.
- **Cancel *both* lines if exiting** — the Collabora add-on renews a day later (8 Oct) and would otherwise continue.
- **Confirmed rolling monthly (2026-09-22).** The contract change page states **"Contract term: 1 month"** and **"Contract term until 08/10/2026"**. This overrides the GTC's *"unless otherwise specified… 12 months"* default ([IONOS GTC](https://www.ionos.co.uk/terms-gtc/terms-and-conditions/) Clause 3), so **there is no 12-month lock-in** — the earlier reading of the GTC was wrong.
- **Notice required:** *"You are entitled to cancel the Services by contacting Us no less than **1 working day prior to the renewal date**"* (GTC Clause 4). With renewal on Wed 7 Oct, the hard deadline is **Tue 6 Oct**; act by **Mon 5 Oct** for buffer.
- **Still to check:** the change page quotes **£9/month**, not the £1 promo rate — confirm on the current invoice whether the **£1/mo × 3 promo is still running** or has already converted.
- **Upshot:** exit is now cheap and repeatable every month, so the provider decision is **no longer time-boxed by lock-in**. It can be made on the merits (T&Cs, export, values) rather than against a contract deadline.

## Cost
~£1/mo × 3 + ~£2/mo Collabora ≈ **£9 for a 3-month pilot** (or less with the 30-day refund). Trivial next to what it de-risks.

## Appendix — pre-sales questions for The Good Cloud (production candidate)
If IONOS fails the app-freedom gate (or on values/T&C grounds), [The Good Cloud](https://thegood.cloud/) is the leading production home. **Ask about the Organisation/Business tier, *not* Consumer** — Consumer is a *personal* Nextcloud account (a Proton-Drive-like personal cloud) and would recreate the "scattered across personal accounts, org owns nothing" problem. Confirm:
1. **Tier & ownership:** an **Organisation** plan = one **org-owned** Nextcloud with central admin + managed member accounts (not personal accounts). Pricing at ~10 users now and at 25–30.
2. **App freedom (the gate IONOS fails):** are **Deck, Collectives, Talk, Collabora/OnlyOffice** all available, and can we install other App Store apps — or is it a curated list?
3. **Group video:** does Talk do **≥10-person calls**, with **external guests via public link**?
4. **Backups:** are **backups included/managed** (frequency, retention), and can we **also pull our own off-site copy** ([ADR-0006](../architecture/0006-backups-and-disaster-recovery.md))?
5. **DPA:** provide the **processor-only DPA** — member data processed only on our instructions, **no marketing/ad use**, EU storage, sub-processor list, retention/deletion terms.
6. **Exit / portability:** on leaving, do we get a **full export / admin / database** for a clean migration (unlike IONOS's no-export lock-in)?
7. **Admin control:** do we get Nextcloud **admin** rights (settings, user provisioning, app management)? Any `occ`?
8. **SLA / continuity:** uptime commitment, support hours, and company size/track record (it is a small B.V. — [R-18](../risks.md)).
9. **Trial:** an Organisation trial, or can we smoke-test on the free 6-month **Consumer** trial (noting its app set may differ from Organisation)?
10. **Custom domain:** can we use **`cloud.bafz.org`** and keep mail (MX) on Proton/Migadu — i.e. **subdomain only, no nameserver takeover**?
11. **Version cadence:** which **Nextcloud / Talk version** do they run today, and how quickly after upstream release do they upgrade? (Threads — a required chat feature — need **Talk 22 / Nextcloud 32 / Hub 25**. IONOS runs **~12 months behind upstream** — tolerable for us, but ask The Good Cloud for their actual lag, since a shorter one is a real advantage. **Also ask: is the version you run still receiving upstream security maintenance, and what is its EOL date?** A year-behind major version is fine; an out-of-support one is not.)
