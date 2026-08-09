# Stack re-evaluation — options paper (August 2026)

- **Status:** Draft for discussion — collates live options; decides nothing on its own
- **Date:** 2026-08-08
- **Author:** Technical admin (with research assistance)
- **Purpose:** A single place to weigh the choices forced open by Hetzner ARM going unavailable, and to reconcile the stack with tools the org already runs (Qomon) and already pays for elsewhere. Feeds decisions back into the ADRs — see the [ADR impact map](#adr-impact-map).

> **Nothing here supersedes an ADR yet.** Each section ends with a recommendation and the ADR it would amend. Promote to the relevant ADR once decided.

---

## TL;DR — recommended path

1. **Host:** move the Nextcloud box to **Netcup VPS 2000 G12** (8 vCPU / 16 GB / 512 GB, ~£198/yr VAT-incl, in stock). Hetzner's June 2026 price rise gutted its x86 value and ARM has been at 0% stock for 30+ days. Amends [ADR-0005](architecture/0005-hosting-provider-and-sizing.md).
2. **Provisioning:** accept a **one-time manual server order** on Netcup (no ordering API exists), then codify DNS + firewall + SSH keys + snapshots with the actively-maintained **`hornc-greedy/netcup`** provider + Ansible — *not* the rincedd providers, which are abandoned (last touched Jan 2021, still `v0.0.1`). Amends [ADR-0010](architecture/0010-vps-provisioning-via-opentofu.md).
3. **Chat:** keep **Nextcloud Talk** as the launch chat (channels + threads, in the box, fastest). Treat **Element/Matrix via `ess-helm`** as a *time-boxed spike*, not a launch commitment — it introduces Kubernetes and reopens bus-factor. Holds [ADR-0002](architecture/0002-chat-layer.md).
4. **Email:** per-branch mailboxes + a central oversight mailbox (Option C), on Migadu **Mini** (not Micro — volume). Amends [ADR-0011](architecture/0011-custom-domain-email-via-migadu.md).
5. **External SaaS:** **Qomon stays** and *shrinks* the self-hosted scope (it owns outward member CRM + mass comms). Reconcile its email sending into the `bafz.org` SPF/DMARC before any mailbox change.
6. **Kanban:** it's **Nextcloud Deck** — another reason Nextcloud stays even if Element is added. See [feature ownership](#feature-ownership--where-each-need-is-met).
7. **New records to keep:** service/vendor inventory, DNS zone register, GDPR RoPA + DPA register, access/offboarding register, incident/breach log. See [records to track](#records--registers-to-track).
8. **If users climb to 50–100:** the maths *inverts* — DIY gets cheaper per head while managed gets pricey, **SSO becomes mandatory** (reopens ADR-0004), Matrix's scale case strengthens, and a solo volunteer admin becomes imprudent. The £250–300 ceiling retires. See *Scale scenario* below.

**Managed Nextcloud is now the leaning launch path** (lowest bus factor at ≤10 users, near-zero ops), with **provider gated on an app-freedom check** — it must install **Collectives + Deck** and run a working office. Shortlist **The Good Cloud** and **Hetzner Storage Share**. **Update: the IONOS real-data pilot PASSED that gate — Deck + Collectives + Collabora all work** (the office error was a browser/Privacy Badger block; older reports were stale) — though the **Talk-threads version gap** (IONOS ~a year behind upstream) and T&C/DPA concerns remain, so The Good Cloud stays the values/backups front-runner. **Netcup DIY** becomes the **on-trigger** target. **Cost headline:** Netcup restores the budget the Hetzner increase broke (~£270–290/yr all-in for the single-stack plan). Adding a *second* self-hosted stack (Element alongside Nextcloud) pushes past the £300 ceiling — that's a committee budget conversation, not an accident.

---

## What changed (the trigger)

Two facts invalidated the assumptions in [ADR-0005](architecture/0005-hosting-provider-and-sizing.md):

- **Hetzner ARM (the CAX line) has been at 0% availability for 30+ days** — not a momentary flap. The CAX31 the whole sizing rested on cannot currently be ordered. ARM scarcity is industry-wide right now (Netcup ARM sold out; Scaleway COP-ARM limited).
- **Hetzner raised prices on 15 June 2026** — "CX/CAX +30–40%, CPX/CCX more than doubled." The AMD CPX line (the x86 fallback in ADR-0005) is now poor value: CPX42 (8/16) ≈ €69/mo net.

Net: the ARM-value thesis that made Hetzner the pick is, for now, unavailable *and* more expensive. That reopens hosting, and with it the provisioning approach.

> All prices below are **VAT-inclusive** to match the budget basis (we cannot reclaim VAT). Netcup lists prices with 19% German VAT; Hetzner lists net, so 19% is added here. GBP at ~£0.855/€. **Verify live before committing** — pricing and stock move.

---

## Decision 1 — Hosting provider (Nextcloud box, ~16 GB)

| Plan | Owner / juris. | vCPU / RAM / Disk | €/mo (VAT-inc) | ~£/yr | Stock |
|---|---|---|---|---|---|
| **Netcup VPS 2000 G12** | 🇩🇪 DE | 8 / 16 GB DDR5 / **512 GB** | **€19.25** | **~£198** | ✅ |
| Hetzner CAX31 (ARM) | 🇩🇪 DE | 8 / 16 GB / 160 GB | €24.98 | ~£256 | ❌ 0%/30d |
| Hetzner CX (Intel, 16 GB) | 🇩🇪 DE | 8 / 16 GB / 160 GB | ~€28–33* | ~£285–330* | ✅ |
| Hetzner CPX42 (AMD) | 🇩🇪 DE | 8 / 16 GB / 320 GB | €82.70 | ~£849 | ✅ |
| OVHcloud (VPS/Public Cloud) | 🇫🇷 FR | ~8 / 16 GB | ~€20–30 | ~£205–310 | ✅ |
| Infomaniak Public Cloud | 🇨🇭 CH | OpenStack, variable | variable | variable | ✅ |

*Intel CX 16 GB price not pinned — verify the live SKU. The AMD CPX line is now disqualified on price.

**All options above are EU/EEA/CH-owned** and pass the sovereignty test; US-owned hosts (DigitalOcean, Linode/Akamai, Vultr) remain excluded by the CLOUD Act reasoning in ADR-0005.

**Why Netcup wins for the Nextcloud box:** cheaper than any *in-stock* Hetzner x86 by ~£90–650/yr; **512 GB disk (3×)** quietly retires the "storage-growth sleeper" risk (R-10) for free; DDR5; no setup fee; hourly *or* 12-month billing; same German jurisdiction as Hetzner. The trade is provisioning (Decision 2) and a more budget-tier support/reputation vs Hetzner's prosumer polish.

### Managed Nextcloud — the ADR-0012 contender, now with providers + pricing
The hosting reopening is the moment to give [ADR-0012](architecture/0012-diy-vs-managed-nextcloud.md) (still *Proposed*) real numbers. Managed Nextcloud attacks our **two largest real costs — volunteer time and bus factor** (the provider patches, upgrades, and backs up), for money now competitive with DIY. The price of that is two hard constraints (infra we control; code-first IaC) and the standing risk that **group video (Talk HPB) and some apps aren't available** — the gating question.

One deliberate exception aside (AccuWeb, flagged below, kept in at the org's request), the list is sovereign-filtered. US-owned providers carry US CLOUD Act / FISA 702 exposure and so fail our sovereignty baseline *regardless of where the data physically sits* — **residency ≠ sovereignty**, exactly the distinction in `CLAUDE.md`.

| Provider | Owner / host | ~£/yr, ≤10 users | ~£/yr, ~25 users | Group video (HPB) | Apps / Deck / Collectives |
|---|---|---|---|---|---|
| **The Good Cloud** ⭐ | 🇳🇱 NL, **EU-owned** (Good Cloud B.V., Utrecht) | verify | verify | N/A at ≤10 | Nextcloud partner → **likely full apps incl. Collectives/Deck** |
| **Hetzner Storage Share** ⭐ | 🇩🇪 DE (our trusted vendor) | ~£45–140 by storage | scales by storage/users | no HPB — **but not needed at ≤10** | full Nextcloud; can add apps — **verify Collectives/Deck** |
| **IONOS Managed Nextcloud** | 🇩🇪 DE | ~£130 (£9/mo +VAT; **£1/mo × 3 promo**) | ~£288 (£20/mo) | Talk 21 — **threads N/A** (needs NC 32; no self-upgrade) | **pilot 2026-08: Deck + Collectives + Collabora all work** ✅ (office "fail" was a browser/Privacy Badger block); **no `occ`**; ~1yr behind upstream |
| **TAB.DIGITAL** | EU-hosted; **ownership unclear** | low per-user (verify) | verify | ✅ HPB add-on | Collabora/ONLYOFFICE/Whiteboard/FTS; Deck/Collectives likely |
| **Portknox** | 🇩🇪 DE, **EU-owned** | verify | verify | ask pre-sales | curated app list |
| **AccuWeb.Cloud** ⚠️ | 🇺🇸 **US company** (EU data-centre option) | pay-as-you-go (usage; verify) | pay-as-you-go | ✅ likely (PaaS) | ✅ **full App Store** — but fails sovereignty |

Prices need a VAT check (some are listed ex-VAT); IONOS runs a launch promo (**1 TB / 10-user tier at £1/mo for 3 months**, then £9/mo).

**Gating verdict — the gate moved.** Your **≤10-person calls with guest links** remove **HPB group video** as a requirement, so it no longer gates provider choice. The *new* gate is **app freedom** — can the managed plan install **Collectives (wiki) + Deck (tasks)** and run a working office suite? Those are required features, and managed plans vary sharply.

**Reality check on IONOS** (Nextcloud community reports): its managed product allows **only a pre-approved app list — no arbitrary installs**, so **Collectives and Deck are likely unavailable** (two required features), **OnlyOffice can't be installed**, **Collabora is reported flaky**, there is **no `occ`**, and users report performance and outdated-version problems. Marketing says otherwise and the reports cite older versions, so treat IONOS as **unverified-but-risky** — a cheap thing to *test* (the £1 trial), not a confirmed launch platform.

**Pilot update (2026-08):** the real-data pilot **disproves the app-freedom fear** — **Deck, Collectives, and Collabora all work** (the "office failed to load" was a **Firefox/Privacy Badger** cross-domain block, not IONOS; older reports were stale). So IONOS is a **legitimate contender**. The one real IONOS gap is **Talk threads (a required feature) — unavailable**: the instance runs Talk 21 / Nextcloud 31, threads need NC 32, and managed = **no self-upgrade** (IONOS is **~a year behind** upstream). Still to test: performance, a 10-person call, and the T&C/DPA gates. Note for rollout: members need a **tracking-protection exception** for office to load (DOC-5). The Good Cloud still leads on values, backups, currency, and clean export.

So the shortlist re-ranks toward **full-Nextcloud managed providers**: **The Good Cloud** (EU-owned, official Nextcloud partner → most likely full apps) and **Hetzner Storage Share** (trusted vendor; its only gap was HPB, now moot at ≤10). Updated rule: **managed wins *if* an EU-owned provider confirms Collectives + Deck + a working office at acceptable cost.**

**On AccuWeb.Cloud (kept in at the org's request):** its pitch — *"private, decentralized, open-source… not just avoiding Big Tech"* — genuinely matches the **ethos** (open-source app, no Google/M365 lock-in, full app freedom, and its PaaS model most likely *can* run HPB, so it clears the app gate cleanly). But it is a **US company**, so US law reaches its data even in an EU data centre — the exact exposure the sovereignty *hard constraint* exists to avoid. It clears the **app** gate but not the **sovereignty** gate. Keep it as an option **only if the committee consciously relaxes the US-jurisdiction constraint** — a premise change worth recording as its own decision — not by mistaking EU data residency for sovereignty.

**Hybrid worth noting:** managed Nextcloud for files/wiki/tasks/calendar/1:1-Talk (offloads all ops) **+ a separate Jitsi** for group video — the exact escape hatch ADR-0012 flags when a managed plan lacks HPB. Costs a small extra Jitsi box but keeps near-zero ops on the heavy part.

**Scale note:** at today's ~10 users, IONOS (~£108/yr) is **cheaper than the DIY server** (~£198/yr) *and* removes ops — managed is genuinely attractive *now*, and only loses its price edge nearer 25–30 users.

**Recommendation:** **managed Nextcloud is the leaning launch path** (lowest bus factor at ≤10 users), **provider gated on an app-freedom check** — shortlist **The Good Cloud** and **Hetzner Storage Share** ahead of IONOS — which **passed the app-freedom gate in the 2026-08 pilot** (Deck + Collectives install) but carries T&C/values concerns (Collabora erroring, data-loss liability disclaimed). **Netcup VPS 2000 G12 (DIY)** becomes the **DIY-on-trigger** target. Amends ADR-0005; **feeds real data into ADR-0012**.

---

## Decision 2 — Provisioning / IaC (the Netcup catch)

Hetzner's appeal for [ADR-0010](architecture/0010-vps-provisioning-via-opentofu.md) was its first-class OpenTofu `hcloud` provider (full create/destroy lifecycle). **Netcup has no server-ordering API at all** — ordering is web-shop only, so *no* provider can create a server. But a community provider recovers most of the rest of the IaC story. Two candidates, and the maintenance signal is decisive:

| Provider | Scope | Latest release | Last commit | Adoption |
|---|---|---|---|---|
| **`hornc-greedy/netcup`** (recommended) | **Unified** — DNS + SCP REST: firewall, SSH keys, snapshots, reverse DNS, failover | **v1.0.0 (Jun 2026)** | **2026-07-22** | 1★ / 0 forks — new, unproven |
| `rincedd/netcup-ccp` + `-scp` | Split — DNS (ccp) + server control/reinstall (scp) | v0.0.1 (Jan 2021) | **Jan 2021** | 16★ + 13★ — but **abandoned ~5y, pre-1.0** |

**Prefer `hornc-greedy/netcup`:** it's current (v1.0.0, commits weeks ago), broader (one provider does DNS **+ firewall + SSH keys + snapshots + reverse DNS** as code — close IaC parity with the old Hetzner firewall/SSH resources), and uses Netcup's newer SCP REST API. The rincedd pair, despite more stars, hasn't been touched since January 2021 and never left `v0.0.1` — five years of Netcup API drift make it a poor bet.

**Resulting pattern:** order the VPS once (manual — no API) → codify firewall + SSH keys + DNS + reverse DNS via `hornc-greedy/netcup` → cloud-init + Ansible for the OS/app layer → snapshot before risky upgrades. Only server *creation* is un-codified; DR ("rebuild") is reproducible via reinstall/snapshot + Ansible on the box we own.

**Caveats:** `hornc-greedy/netcup` is a single-author, 1-star project — the "fresh but unproven" trade (a small irony for a bus-factor-conscious org). Mitigate: it's MPL-2.0, so **pin the exact version and vendor/mirror the binary**; the universal fallback for any Netcup provider is the SCP/CCP web panel by hand (config, not data — recoverable). Also **verify it can trigger an OS reinstall** (rincedd-scp's DR trick); if not, its snapshots-as-code is an equal-or-better DR primitive. Net: ADR-0010 moves from "OpenTofu creates everything" to "OpenTofu owns DNS + firewall + SSH + snapshots + rDNS; the initial server order is a one-time manual click."

**Recommendation:** `hornc-greedy/netcup`, pinned + mirrored. Amends ADR-0010.

---

## Decision 3 — Chat (and the Element question)

Requirement: channels, membership, replies, **threads**. Three shapes, differing mostly in *how many stacks we run*:

| Path | Runs | Channels+threads | Ops surface | ADR impact |
|---|---|---|---|---|
| **A. Nextcloud + Talk** | 1 stack (Docker AIO) | ✅ today | Lowest | host swap only |
| **B. Element now, Nextcloud later** | k3s cluster now | ✅ best-in-class | +Kubernetes | supersede 0002, touch 0009 |
| **C. Both, deliberately** | k3s **and** Docker AIO | ✅ | Highest — two stacks | supersede 0002, reopen 0009 |

**Element via `ess-helm` — the facts:** `ess-starter-edition-core` is **deprecated** (24.10); `ess-helm` on single-node **k3s** is the blessed path — a documented ~6-step quickstart (Synapse, Matrix Authentication Service, Element Web/Admin, Element Call/Matrix RTC, Postgres, HAProxy). Min 2 CPU / 2 GB; realistically 4 GB text-only, 8 GB with Element Call. Matrix gives arguably *better* Slack-like channels/threads than Talk.

**The honest catch:** B/C mean **owning Kubernetes and (eventually) two stacks** on a bus-factor-1 org — the exact exposure ADR-0002/0009 protect against. And "fastest chat" points *away* from Element: **Talk is already in the AIO box**, zero extra services. Standing up k3s is slower to a working chat, not faster.

**Exploring is cheap; adopting is the question.** Both Netcup and Hetzner bill hourly — an 8 GB Element spike run for a 2-week evaluation costs ~€4–5, then destroy it. That's the right way to test the k8s appetite before committing.

**Recommendation:** **Talk at launch** (holds ADR-0002). Run an Element spike only as a *time-boxed evaluation*; promote to a superseding ADR only if the org accepts owning Kubernetes.

### Considered and set aside: Proton as the files/calendar backbone
"Everyone has Proton, use it for shared resources + Element for chat" was considered. It's a coherent *different philosophy* (privacy-via-trusted-SaaS) but conflicts with the project premise:

- **Personal Proton accounts rebuild the exact antipattern the proposal condemns** — data scattered across individuals' accounts, leaving when they leave. No org-owned home.
- **Org ownership needs Proton for Business** — per-seat (~£500–1,300/yr for 5–10 people) → **busts the £250–300 ceiling**; and we get no nonprofit discount (not a registered nonprofit).
- **It's still SaaS** → fails the "infra we control" hard constraint (jurisdiction-sovereign, not infrastructure-sovereign).
- **It only covers ~1.5 of 6 features** — no chat, no wiki, no tasks; **Proton Calendar has no open CalDAV** (misses the stated requirement); Docs ≠ a structured wiki.
- **Backwards for bus factor:** it offloads the *easy* self-hosted part (Nextcloud) and keeps the *hard* part (self-hosted Matrix).

**Recommendation:** keep Proton in its current role (Pass vault, [ADR-0007](architecture/0007-secrets-management.md)); do **not** make it the Drive/Calendar backbone. If the committee's priority genuinely shifts from "own the infra" to "least admin effort," that's a premise change to record as its own ADR.

---

## Decision 4 — Email / mailbox topology (branches)

Migadu bills flat-fee with **unlimited mailboxes and aliases per domain** — so mailbox *count* is free. The real limit is **account-wide daily volume** (Micro: 20 out / 200 in per day; **Mini: 100 out / 1,000 in**). Design on **access & governance**, not cost.

The requirement pulls two ways: *"each branch has its own address → folders"* (sounds single-mailbox) vs *"central team can monitor **and control** each branch's mailbox"* (sounds separate mailboxes). Three resolutions:

- **A — One shared mailbox + branch aliases → Sieve folders.** Cheap, trivial central view, but **no isolation** (shared login; one leak exposes all branches).
- **B — Per-branch mailboxes; central holds the keys** (passwords in the BAFZ Vault). Real isolation + control, but no passive single-pane view.
- **C — Hybrid (recommended): per-branch mailboxes + a central `oversight@` that gets a Sieve `redirect :copy`,** filed per-branch into folders. Each branch gets its own address + isolation *and* the central team gets the "everything in folders" view *and* full control via vault'd credentials.

**Caveats:**
- **Migadu has no per-folder ACL / delegation** — access to a mailbox = its credentials. Design leans on aliases + copies + vault'd passwords, not delegated access.
- **Tier:** 4 branches of human correspondence will likely exceed Micro's 20 sends/day → **Mini (~£70/yr)**, a ~£55/yr delta on ADR-0011's ~£15/yr assumption. (Mass member email is Qomon's job, *not* Migadu's — see Decision 5 — which keeps Migadu volume modest.)
- **GDPR:** central read-access to branch mail must be disclosed to branch users (one-line notice).

**Sequencing gate:** `bafz.org` is **already live on Proton Mail** in production (real MX, three Proton DKIM selectors, DMARC `p=reject`) — per zac343's audit on issue #58. This is a **migration, not a greenfield setup**: provision Migadu + publish its DKIM *alongside* Proton, prove delivery, then cut MX over with a rollback window.

**Recommendation:** Option C on Migadu **Mini**, executed as a migration. Amends ADR-0011.

---

## Decision 5 — External SaaS boundaries (Qomon, Proton)

**Model:** Qomon is **outward-facing** (supporters, members-as-contacts, donors, public); the self-hosted stack is **inward-facing** (the team's own operations). They barely compete — Qomon does **none** of chat/files/wiki/voice-video — but collide in one place: **email on `bafz.org`**.

| Qomon does | Stack equivalent | Verdict |
|---|---|---|
| Supporter/member/donor **CRM** | Nextcloud Contacts | Qomon = system of record; Contacts = internal address book only |
| **Email/SMS campaigns** | Migadu, ADR-0008 relay | Collision on the sending domain (below) |
| **Events** / Action Hub (RSVP) | Nextcloud Calendar | Qomon = public/volunteer events; Nextcloud = internal calendar/rota (CalDAV) |
| **Tasks/actions**, forms, petitions | Deck, Nextcloud Forms | Qomon = campaign actions; Deck = internal team board |
| Fundraising, canvassing, phone-bank, mapping | — | Pure gap-fill — keep Qomon |
| Chat, files, wiki, voice/video | Talk, Nextcloud | Zero overlap — the point of the self-hosted stack |

**The one real collision — senders on `bafz.org`.** Once Migadu lands, the domain has 4+ outbound systems: **Migadu** (1:1 human mail), **ADR-0008 relay** (Nextcloud transactional), **Qomon** (`qomon.email`, mass member mail), and **`sendersrv.com`** (an *unknown* existing sender — identify it), plus Proton currently live. Consequences:
- **SPF has a hard 10-DNS-lookup limit** — four `include:`s risk `permerror` → mail fails under the existing `p=reject`. May need SPF flattening / dropping dead senders. This is ADR-0011's sharp edge, made sharper.
- **DMARC alignment per sender** — if Qomon sends *as* `@bafz.org`, its DKIM must be published in the zone and aligned, or campaigns fail `reject`.

**Boundaries to write down (so we don't fragment or double-pay):**
- **Member data system-of-record = Qomon.** Don't duplicate members into Nextcloud (two sources of truth doubles GDPR surface). Qomon is French/EU (good jurisdiction) but SaaS with US operations — do a DPA/transfer check.
- **Events:** public/volunteer → Qomon; internal rota (CalDAV) → Nextcloud.
- **Tasks:** campaign actions → Qomon; internal kanban → Deck.

**Reinforcing insight:** Qomon being the mass-send channel is *why* Migadu's small send limits are fine — never mass-mail from Migadu. Qomon also **shrinks the self-hosted scope** (no need to build CRM/comms/fundraising in Nextcloud), which lowers bus-factor load.

**Recommendation:** keep Qomon; add an "external SaaS boundaries" note to the architecture and fold the Qomon sender into ADR-0011's SPF/DMARC design.

---

## Feature ownership — where each need is met

Answers "which part of the stack gives a Kanban board": **Nextcloud Deck.**

| Required feature | Owned by | Notes |
|---|---|---|
| Text chat (channels/threads) | **Nextcloud Talk** (or Element, if adopted) | Talk meets it in-box today |
| **Task Kanban board** | **Nextcloud Deck** | Trello-style boards/lists/cards/labels/due-dates; part of the AIO backbone (ADR-0001). Element/Matrix has **no** Kanban — if we ever went Element-only we'd need a separate tool (Vikunja/Planka/Wekan). Qomon's tasks are campaign actions, not an internal board |
| Wiki / knowledge base | **Nextcloud Collectives** | |
| File store (sync + share) | **Nextcloud Files** | 512 GB on Netcup gives real headroom |
| Voice / video | **Talk + HPB** (Jitsi fallback) | ADR-0003 |
| Shared calendar (CalDAV) | **Nextcloud Calendar** | Qomon events are separate/outward |
| Human `@bafz.org` mailboxes | **Migadu** | Decision 4 |
| Member/supporter CRM + mass comms + fundraising | **Qomon** | Outward-facing; not in the self-hosted stack |

**Deck is a concrete reason Nextcloud stays even if Element is added** — Element cannot replace it.

---

## Cost scenarios vs the ~£250–300 ceiling (at today's ~10 users)

| Scenario | Hosting /yr | + domain/vault/email/backups* | Total |
|---|---|---|---|
| **DIY Nextcloud + Talk** (Netcup VPS 2000) | ~£198 | ~£145 | **~£343** (~£290 if Migadu Micro suffices) |
| **Managed Nextcloud + Talk** (IONOS) | ~£108 (≤10) – £240 (~25) | ~£125** | **~£233 now – £365 at 25** — near-zero ops |
| **Element only** (Netcup VPS 1000, chat-only org) | ~£106 | ~£145 | ~£251 |
| **Both self-hosted** (VPS 2000 + VPS 1000) | ~£304 | ~£145 | **~£449** — over |

*Domain ~£13, Proton Pass ~£42, backups ~£20, **Migadu Mini ~£70** (or ~£17 at Micro if branch 1:1 volume is low — a £53 swing). Plus Hetzner→Netcup FX/card fees.
**Managed: the provider backs up, so the £20 self-hosted-backup line is optional (kept for an own off-site copy per [ADR-0006](architecture/0006-backups-and-disaster-recovery.md)).

Takeaways: **Netcup pulls the DIY server line back under control** after the Hetzner increase; **managed Nextcloud is cheaper than DIY at today's ~10 users** and only loses that edge nearer 25; and **two self-hosted stacks breach the ceiling** — a committee budget decision, not a silent drift. How this inverts at 50–100 users is its own section below.

## Scale scenario — what changes at 50–100 users

The £250–300 ceiling and single-box sizing are *small-org* assumptions. At 50–100 users several things move at once, and some **reverse**:

- **Compute & storage.** 16 GB (Netcup VPS 2000) is sized for 20–30. At 50–100 you move to **Netcup VPS 4000 (32 GB, ~£333/yr)** or **VPS 8000 (64 GB, ~£492/yr)**, and likely **split services** (Collabora and the Talk HPB onto their own boxes) — the AIO single-box model starts to strain. File growth pushes the primary data store toward **S3-compatible object storage** on a sovereign provider, and a larger BorgBase backup tier.
- **The cost curve inverts.** Managed Nextcloud is *cheaper than DIY at 10 users but far pricier at 100*: IONOS at 50 users is ~£540/yr and climbs; a single 64 GB DIY box serving 100 is ~£492/yr (~£5/user/yr). So **DIY's cost advantage returns at scale** — while the **bus-factor/ops argument for managed intensifies** (one volunteer running a multi-service stack for 100 people is imprudent). That tension, not price, becomes the deciding factor.
- **SSO stops being optional — reopens [ADR-0004](architecture/0004-identity-and-sso.md).** Hand-provisioning 100 accounts across Nextcloud, Talk/Matrix, and email — and *de*-provisioning on exit — is untenable and a security/GDPR risk. An **IdP (Keycloak / Authentik / Zitadel)** with SSO becomes near-mandatory.
- **Chat: the Matrix calculus shifts — [ADR-0002](architecture/0002-chat-layer.md).** Talk is fine for chat at any size, but its group-video (HPB) load at 50–100 is heavy; Matrix/Synapse is *built* for large communities (spaces, big rooms, federation), so the richer chat ADR-0002 deferred starts to justify itself — at the cost of Synapse-at-scale ops (workers, tuning) that again point to *managed* Matrix.
- **Email.** Migadu mailboxes stay flat-fee (a plus), but the account-wide daily send/receive limits push you to **Standard (~£240/yr)**. Mass member email stays on Qomon regardless.
- **Governance & availability.** 50–100 members' data makes the RoPA/DPA/access registers a firmer legal duty, and downtime hurts more people — HA (still costly) moves from "out of scope" to "worth pricing."

**Bottom line:** 50–100 users is past the point where a bus-factor-1 volunteer *should* run this solo. The realistic shapes become **(a) DIY on a bigger split-service box + a real admin team + SSO**, or **(b) managed Nextcloud/Matrix**, accepting the higher fee for continuity. Either way the **£250–300 ceiling is retired** in favour of a per-user budget — and this should trigger a committee conversation *well before* the org reaches that size, not at it.

---

## Records & registers to track

The repo already holds the **risk register** (`risks.md`), **ADRs** (decision records), and the **restore runbook**. Gaps worth filling, most valuable first:

| Record | Why | Where | Priority |
|---|---|---|---|
| **Service & vendor inventory** | Every service/vendor, jurisdiction, purpose, cost, renewal date, billing owner, where creds live — core bus-factor + budget artifact | `docs/reference/` | **High** |
| **DNS / zone register** | Authoritative source-of-truth for MX/SPF/DKIM(×N senders)/DMARC/A/AAAA — directly de-risks the 4-sender SPF collision | `docs/reference/` | **High** |
| **GDPR RoPA + DPA register** | UK GDPR Art 30 (record of processing) + Art 28 (processor agreements) — member PII spans Qomon, Migadu, Nextcloud, BorgBase; likely a legal duty | `docs/reference/` or wiki | **High** |
| **Secrets index** | What *should* live in the Proton Pass vault (an index, not the secrets) — makes the vault auditable | ties to ADR-0007 | **High** |
| **Backup/restore test log** | Evidence of tested restores (launch blocker #2/#3) | runbook-adjacent | **High** |
| **Access + offboarding register** | Who has access to what; revoke-on-leave — solves the "someone leaves" continuity/GDPR problem | `docs/reference/` or wiki | Medium |
| **Incident & data-breach log** | GDPR Art 33 needs a breach record (72h notification) | wiki | Medium |
| **Renewals / billing calendar** | Domain, Migadu, Proton, Netcup, Qomon, backups — prevent lapse; track FX exposure | the Nextcloud calendar, once live | Medium |
| **Decision / committee log** | Budget approvals, the second-admin naming (GOV-7) | wiki | Medium |
| **2nd-admin onboarding runbook** | ADR-0009 obligation; extend the existing Pass-onboarding runbook | `docs/runbooks/` | Medium |

Rule of thumb: **in-repo** for anything code-adjacent or that a second admin needs before the stack exists (inventory, DNS, RoPA); **Nextcloud wiki** for living operational logs once it's up; **Proton Pass vault** for the secrets themselves (index only in-repo).

---

## ADR impact map

| Decision | ADR action |
|---|---|
| Host → Netcup | **Amend/supersede [ADR-0005](architecture/0005-hosting-provider-and-sizing.md)** (provider, sizing, price-increase reality) |
| Provisioning pattern | **Amend [ADR-0010](architecture/0010-vps-provisioning-via-opentofu.md)** (Netcup: manual order + `hornc-greedy/netcup` for DNS/firewall/SSH/snapshots + Ansible) |
| Chat = Talk; Element as spike | **Holds [ADR-0002](architecture/0002-chat-layer.md)**; a superseding ADR only if Element/k8s is adopted (touches [0009](architecture/0009-bus-factor-and-second-admin.md)) |
| DIY vs managed Nextcloud | **Feeds provider + pricing data into [ADR-0012](architecture/0012-diy-vs-managed-nextcloud.md)**; still gated on a sovereign provider confirming Talk HPB group video |
| Scale to 50–100 users | **Reopens [ADR-0004](architecture/0004-identity-and-sso.md)** (SSO), re-weights [ADR-0002](architecture/0002-chat-layer.md) (Matrix) and [ADR-0005](architecture/0005-hosting-provider-and-sizing.md) (sizing/split services); retires the £250–300 ceiling |
| Proton-as-backbone | **New ADR** recording it as considered/rejected (touches CLAUDE.md premise, [0007](architecture/0007-secrets-management.md)) |
| Mailbox topology | **Amend [ADR-0011](architecture/0011-custom-domain-email-via-migadu.md)** (Option C, Mini-tier cost, no-delegation, migration gate) |
| Qomon boundaries + senders | **Amend [ADR-0011](architecture/0011-custom-domain-email-via-migadu.md)** (4-sender SPF/DMARC) + an architecture note on external-SaaS boundaries |
| New records/registers | Create `docs/reference/`; update `CLAUDE.md` cost summary + `risks.md` |

---

## Open decisions / next actions

1. **Confirm Netcup** as the host and re-verify its live VAT-inclusive price + the Migadu Mini tier. → amend ADR-0005, ADR-0011 cost lines, `CLAUDE.md`.
2. **Decide chat direction:** Talk-only for launch (recommended) vs a funded Element spike. → holds or supersedes ADR-0002.
3. **Identify `sendersrv.com`** and inventory all `bafz.org` senders; design one combined SPF + DKIM set (Migadu + relay + Qomon). → amend ADR-0011.
4. **Reconcile Proton Mail already being live** with the Migadu plan — migrate or retain? → ADR-0011 migration section.
5. **Run the £1 IONOS pilot as the app-freedom test** (can it install **Collectives + Deck**, run Collabora, and do a 10-person call with a guest?) — see the [pilot runbook](runbooks/managed-nextcloud-pilot.md). If IONOS fails, pivot to **The Good Cloud** / **Hetzner Storage Share** (30-day money-back caps the risk).
6. **Stand up `docs/reference/`** with the high-priority registers before production data lands.
