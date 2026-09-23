# Secrets index — BAFZ Vault

An **index of what should live in the BAFZ Vault** (Proton Pass Family, [ADR-0007](../architecture/0007-secrets-management.md)) — names and purposes only, **never the values**. Makes the vault auditable and gives a second admin a checklist of what recovery requires. The vault itself is off the infrastructure it protects.

| Item | Purpose | Present? |
|---|---|---|
| Nextcloud provider admin login | manage the managed instance (IONOS pilot → prod) | ✅ present — **includes the instance URL** |
| Nextcloud app password ("Claude Nextcloud App") | scripted administration over the OCS API without `occ` | ✅ present (2026-09-22) — revocable from Settings → Security |
| Domain registrar credentials | control `bafz.org` | **TODO — org doesn't control the domain yet (R-29)** |
| Migadu account + mailbox app-passwords | `@bafz.org` mail | TODO (planned) |
| Qomon login | outreach CRM | TODO |
| Proton account (holds the vault) | recovery of the vault itself | TODO — document recovery method |
| Healthchecks.io | monitoring/alerts | TODO |
| Transactional relay creds (Scaleway/Mailjet) | Nextcloud system mail | TODO |
| **DIY-on-trigger only:** | | |
| Netcup login | self-hosted host | TODO (on-trigger) |
| VPS root / SSH key | server access | TODO (on-trigger) |
| BorgBase login **+ Borg key/passphrase** | off-site backup — **unrecoverable without the key (R-05)** | TODO (on-trigger) |

**Rule:** every credential the org would need to recover the stack lives here, added the moment the account is created — not retrofitted.

**Also record the URL.** A username and password with no address is not recoverable — a second admin needs to know *what* the credential unlocks, not just how to unlock it. Every item gets the login URL alongside the secret. On the managed path the **day-one own-copy sync** location/credentials also belong here (it is our only backup — R-25).
