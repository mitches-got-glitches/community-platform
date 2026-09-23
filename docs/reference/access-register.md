# Access register

Who has an account on which system, what they can reach, and when access was granted or removed. Needed for **offboarding** (DOC-8), and for answering *"who can see members' information?"* under UK GDPR — a question we must be able to answer, not estimate.

## ⚠️ The register itself lives outside this repo

**This repository is public.** A list of members' names against the systems they can access is personal data, and publishing it would be a disclosure in its own right — as well as a map of the org's attack surface.

So this file holds the **structure and the rules**. The populated register lives in:

- the **Admin guides** collective (admin-Team only), for day-to-day use, **or**
- the **BAFZ Vault**, if it is ever to include anything credential-adjacent.

Keep the columns below identical in whichever copy is authoritative, so this file stays a usable spec.

## Columns

| Column | Notes |
|---|---|
| Person | Display name — no contact details, those live in the CRM |
| Account | Nextcloud login name (permanent once set) |
| Teams | e.g. BAFZ East, Admin guides — drives wiki visibility |
| Groups | Nextcloud groups, where used |
| Talk channels | Only those needing deliberate membership |
| Other systems | Migadu mailbox, Qomon, vault seat, provider console |
| Granted | Date |
| Requested/approved by | Who asked — the accountability trail |
| Removed | Date, blank while active |

## Rules

- **Add the row when the account is created**, not later. A register reconstructed from memory is not a register.
- **Never delete a row** — fill in *Removed*. Knowing who *used to* have access is the point during an incident.
- **Review at least twice a year**, and always after someone steps back from a role.
- **Admin-level access is listed explicitly**, including the provider console and the vault seat — those are the credentials that matter if someone leaves under strain.
- **Offboarding is not complete until every row for that person has a *Removed* date** — see DOC-8.

## Systems to cover

Nextcloud (accounts, Teams, groups) · Talk channels · **IONOS provider console** · **BAFZ Vault seats** · Migadu mailboxes · Qomon · domain registrar (once org-controlled — R-29).
