# Reference

Dry, factual registers with no narrative — the Diátaxis *reference* quadrant (see [`../README.md`](../README.md)). Kept current as facts change; link decisions to the ADRs rather than restating them here.

| Doc | What it records |
|---|---|
| [service-inventory.md](service-inventory.md) | Every service/vendor, jurisdiction, cost, renewal, owner, and where its credentials live |
| [dns-zone.md](dns-zone.md) | The `bafz.org` DNS records — especially the multi-sender mail records |
| [ropa.md](ropa.md) | UK GDPR Record of Processing Activities (Art 30) + Data Processing Agreement register |
| [secrets-index.md](secrets-index.md) | Index of what lives in the BAFZ Vault (names only — never values) |
| [managed-hosting-limits.md](managed-hosting-limits.md) | What managed hosting prevents us doing, what it has cost, and what substitutes — evidence for the ADR-0012 exit triggers |

**Status:** scaffolded 2026-08-08. Seeded rows are provisional; `TODO` marks what to confirm. The RoPA + DPA register and the processor DPAs are **required before real member data lands** — see **R-15 / R-26** in [`../risks.md`](../risks.md).
