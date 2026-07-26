# Onboarding/offboarding admins on the BAFZ Vault (Proton Pass Family)

How to add or remove an admin's access to the shared **BAFZ Vault**, and how to install
and authenticate the Proton Pass CLI (`pass-cli`) for scripts/automation that need to read
a secret (e.g. the Hetzner API key) without a human opening the app.

**Last updated:** 2026-07-26

**Owner:** technical admin

---

## Table of Contents

- [When to use this](#when-to-use-this)
- [Before you start](#before-you-start)
- [Add a new admin to the vault](#add-a-new-admin-to-the-vault)
- [Remove an admin's access](#remove-an-admins-access)
- [Install and log in with pass-cli](#install-and-log-in-with-pass-cli)
- [Read a secret with pass-cli](#read-a-secret-with-pass-cli)
- [Record of who has access](#record-of-who-has-access)
- [References](#references)

---

## When to use this

- A new admin or committee member needs access to the org's infrastructure secrets
  (VPS root/SSH, domain registrar, Borg backup key, SMTP relay, Migadu, Hetzner API key).
- An admin is stepping down and their access must be revoked.
- You need `pass-cli` on a machine to script something against a stored secret (e.g. feed
  the Hetzner API key to OpenTofu) instead of copy-pasting it out of the app.

This is *account/access* administration for the vault itself. For what's actually stored
in it and why, see [ADR-0007](../architecture/0007-secrets-management.md).

## Before you start

- The vault is hosted on a **dedicated org Proton account** (not a personal admin
  account), on the **Pass Family** plan — see [ADR-0007](../architecture/0007-secrets-management.md)
  for why. Whoever holds the vault-owner login is the one who sends invites.
  - "Dedicated" means: an account created *for this role*, not reused from someone's
    personal inbox — its login shouldn't need to move with a specific person. A fresh
    address like `mitch-bafz@proton.me` is a fine starting point (that's what exists
    today); the important part is treating it as an org asset from day one, not "Mitch's
    account that the org also uses." Two follow-ups worth doing when there's time, not
    blockers to using it now:
    - Point its **recovery email** at something org-controlled (a Migadu `@bafz.org`
      address once [ADR-0011](../architecture/0011-custom-domain-email-via-migadu.md) is
      live) rather than a personal inbox.
    - **The vault-owner account's own login + 2FA recovery codes can't live inside the
      vault they unlock** — same chicken-and-egg problem as the Borg key ([ADR-0007]).
      Record them out-of-band (written down and stored physically, or handed directly to
      the second admin once recruited per [ADR-0009](../architecture/0009-bus-factor-and-second-admin.md))
      rather than leaving them recoverable only via one person's personal phone/email.
- Know the access level you intend to grant (see below) — decide this *before* sending
  the invite, not after.
- The new person needs a Proton account of their own (a free account is enough) — sharing
  never means handing out the vault-owner's own login.

**Access levels** (choose deliberately, don't default to the top one):
- **Viewer** — can see and use items, can't change or share them. Right for anyone who
  only needs to *read* a secret occasionally.
- **Editor** — can view and edit items, create new ones. Right for an active co-admin.
- **Manager** — full control, including sharing the vault with others and removing
  members. Reserve this for the actual second admin from [ADR-0009](../architecture/0009-bus-factor-and-second-admin.md),
  not every occasional helper — a vault where everyone is a manager has no accountability
  trail for who added or removed whom.

## Add a new admin to the vault

Sharing a vault is done from the **app or browser extension**, not `pass-cli` (the CLI has
no vault-membership commands — it's for reading/writing items once you already have
access).

1. Log into the Proton Pass app/extension as the **vault owner** (the dedicated org
   account, not a personal one).
2. Open **BAFZ Vault** → the vault's options menu (⋮) → **Share**.
3. Enter the new admin's Proton account email, choose their access level (Viewer /
   Editor / Manager — see above), and continue.
4. Confirm and send. The invite arrives as an in-app notification (if they already have a
   Proton account) or an email invite to create one.
5. Once they accept, update the [record of who has access](#record-of-who-has-access)
   below in the same session — don't let this drift.

## Remove an admin's access

1. As the vault owner (or a Manager), open **BAFZ Vault** → **Share** → the member list.
2. Remove the departing admin from the member list. This revokes their access
   immediately; it does not rotate the secrets themselves.
3. **Rotate anything they could have exfiltrated** while they had access — at minimum the
   Hetzner API key and any credential with write/destructive scope (VPS root, registrar).
   Removing vault access stops *future* reads, not past ones.
4. Update the [record of who has access](#record-of-who-has-access) below.

## Install and log in with pass-cli

Linux/macOS:

```bash
curl -fsSL https://proton.me/download/pass-cli/install.sh | bash
```

Windows (PowerShell):

```powershell
Invoke-WebRequest -Uri https://proton.me/download/pass-cli/install.ps1 -OutFile install.ps1; .\install.ps1
```

Log in (opens a browser for web-based auth by default):

```bash
pass-cli login
```

Use `pass-cli login --interactive` instead if you want to authenticate with
username/password on the command line rather than a browser flow (e.g. a headless box).

Verify you can see the shared vault:

```bash
pass-cli vault list
```

`BAFZ Vault` should be in the output. If it isn't, your account hasn't been added as a
member yet — see [above](#add-a-new-admin-to-the-vault).

## Read a secret with pass-cli

List items in the vault to confirm the item name:

```bash
pass-cli item list --vault-name "BAFZ Vault"
```

View a specific item (e.g. the Hetzner API key):

```bash
pass-cli item view --vault-name "BAFZ Vault" --item-name "Hetzner API Key"
```

For scripting, reference the secret directly rather than copy-pasting it into a script or
shell history:

```
pass://BAFZ Vault/Hetzner API Key/password
```

Check `pass-cli`'s own `--help` for the exact secret-reference syntax your installed
version supports — the CLI is under active development and flags can change between
releases; don't assume the above is pinned.

> Treat any machine that's run `pass-cli login` as holding a credential in its own right.
> Log out (`pass-cli logout`) on shared or temporary machines, and don't leave a logged-in
> session on anything that isn't yours to keep secured.

## Record of who has access

Keep this table current — it's the fast answer to "who can see our secrets right now,"
which matters for both routine audits and an offboarding in a hurry.

| Name | Proton account (email) | Access level | Added | Removed |
|------|------------------------|---------------|-------|---------|
| Mitch | (vault owner — dedicated org account) | Manager | 2026-07-26 | |

## References

- [ADR-0007: Secrets management](../architecture/0007-secrets-management.md) — why Pass,
  why a dedicated org account, what's stored.
- [ADR-0009: Bus factor and second admin](../architecture/0009-bus-factor-and-second-admin.md)
  — who should hold Manager access and by when.
- [Proton Pass CLI documentation](https://protonpass.github.io/pass-cli/)
- [Restore runbook](restore.md) — where these same secrets get *used*, not just stored.
