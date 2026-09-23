# Ansible — host configuration

Configures the bare VPS that [OpenTofu](../infra/opentofu/) provisions: Docker, Caddy,
and Nextcloud AIO, per [ADR-0001](../docs/architecture/0001-nextcloud-backbone-and-deployment.md).
This is the IaC spine — issue #12 (INFRA-3) — currently a skeleton: `common` runs real
baseline setup, `docker`/`caddy`/`nextcloud_aio` are structural placeholders filled in by
later Epic A tickets, and `roles/hardening/` is reserved but empty (INFRA-4, #13, per
[ADR-0008](../docs/architecture/0008-operational-baseline.md) — not built here).

**Scope boundary:** this starts where OpenTofu stops (the OS up). VPS/network creation is
OpenTofu's job (ADR-0010), not Ansible's.

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/) — manages a pinned,
  reproducible `ansible-core` install for this directory (`pyproject.toml` + `uv.lock`),
  so you don't depend on whatever Ansible version your OS package manager happens to ship.
  `gwt-add` (if you use the dotfiles worktree helpers) runs `uv sync` here automatically
  when you create a worktree for this repo.
- An SSH key authorised on the target host (the same public key OpenTofu put on the
  server — see [`infra/opentofu/README.md`](../infra/opentofu/README.md)).
- The [Proton Pass CLI](https://protonpass.github.io/pass-cli/) (`pass-cli`) for any
  secret this playbook needs at run time — see [Secrets](#secrets) below.
- A provisioned host and its IP from `tofu output server_ipv4` (see
  [`infra/opentofu/README.md`](../infra/opentofu/README.md)) — until INFRA-2 lands, the
  inventory holds a placeholder address and runs can only go as far as `--check`.

## One-command run

From the repo root, via the [justfile](../justfile):

```sh
just ansible-check   # dry run — --check, no changes made
just ansible-apply    # apply for real
```

Equivalent by hand, from this directory:

```sh
uv sync                              # once, or after pyproject.toml/uv.lock changes
uv run ansible-playbook site.yml --check
uv run ansible-playbook site.yml
```

Before either, update [`inventory/production.yml`](inventory/production.yml)'s
`ansible_host` with the real server address:

```sh
tofu -chdir=../infra/opentofu output -raw server_ipv4
```

## Layout

- **`site.yml`** — the one playbook; applies every role to every host.
- **`inventory/production.yml`** — the single target host (see above).
- **`group_vars/all/`** — variables shared by every host: `vars.yml` for non-secret
  config, `secrets.yml` documenting the secret-resolution pattern (see below).
- **`roles/`** — one role per concern: `common` (baseline OS setup — real), `docker`,
  `caddy`, `nextcloud_aio` (placeholders, filled in by later Epic A tickets), `hardening`
  (reserved, not wired into `site.yml` yet — see the role's own `README.md`).

## Secrets

Per [ADR-0007](../docs/architecture/0007-secrets-management.md), **no secret is ever
committed in plaintext** — not in `group_vars`, not anywhere else in this repo. Nothing
in this skeleton currently needs one (the roles that will — `nextcloud_aio`'s admin
password, an SMTP relay credential — are still placeholders), but the pattern to follow
when that changes, matching what `just tofu-plan`/`just tofu-apply` already do for
`HCLOUD_TOKEN`:

1. Add the variable to `group_vars/all/secrets.yml` as an environment-variable lookup:
   ```yaml
   some_secret: "{{ lookup('ansible.builtin.env', 'SOME_SECRET') }}"
   ```
2. Store the real value in the Proton Pass vault ("BAFZ Vault").
3. Resolve it at run time through `pass-cli`, never a shell export or a `.env` file:
   ```sh
   SOME_SECRET="pass://BAFZ Vault/<item>/<field>" pass-cli run -- uv run ansible-playbook site.yml
   ```
4. Add a `just` recipe for it (see [`../justfile`](../justfile)) rather than leaving the
   invocation as a copy-paste snippet.

## Idempotency

The playbook is safe to re-run — re-applying it reconciles the host with what's in git
rather than reprovisioning from scratch.
