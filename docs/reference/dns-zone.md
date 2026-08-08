# DNS zone register — `bafz.org`

Source-of-truth for the `bafz.org` DNS records. The apex mail records are **live in production on Proton Mail**; changing them wrongly breaks mail, so this register exists to make every record deliberate — especially the multi-sender setup (R-27). We do **not** currently control this zone (R-29); changes go via the domain admin for now.

> **Golden rule:** never change nameservers or the apex `MX`/`SPF`/`DKIM`/`DMARC` casually. SPF must be **one** TXT record; the domain has a **10-DNS-lookup** budget across all `include:`s.

## Apex (`bafz.org`) — mail (LIVE, Proton)
| Type | Value | Purpose | Status |
|---|---|---|---|
| MX | `mail.protonmail.ch` / `mailsec.protonmail.ch` | inbound mail | **live** — do not disturb until Migadu cutover |
| TXT (SPF) | `v=spf1 include:_spf.protonmail.ch include:sendersrv.com include:qomon.email ...` | authorised senders | live — **`sendersrv.com` unidentified (TODO)** |
| CNAME | `protonmail`, `protonmail2`, `protonmail3` selectors | Proton DKIM | live |
| TXT (DMARC) | `_dmarc` → `p=reject; rua=...` | policy | live — reject; every sender must align |
| TXT | Proton domain-verification | ownership | live |

## Planned changes (Migadu migration — [ADR-0011](../architecture/0011-custom-domain-email-via-migadu.md), issue #58)
Staged, with rollback — provision Migadu + publish its DKIM alongside Proton, prove delivery, then switch MX. The **combined SPF** must list Migadu + the transactional relay + **Qomon** (+ retire dead senders to stay under 10 lookups). TODO: build and validate the single combined SPF before cutover.

## Subdomains
| Name | Type | Target | Purpose | Status |
|---|---|---|---|---|
| `cloud.bafz.org` | A/CNAME | Nextcloud instance | collaboration app URL | **TODO** — pilot may use IONOS default hostname instead (we don't control DNS yet — R-29) |

**TODO:** identify `sendersrv.com`; obtain zone control or a working change path with the domain admin; record the final combined SPF here once built.
