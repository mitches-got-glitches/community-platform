# OpenTofu — Hetzner VPS provisioning

Declares the box Ansible (INFRA-3 onward) configures: the Hetzner CAX31 server, an SSH
key resource, and a Cloud Firewall (22/80/443 only). See
[ADR-0010](../../docs/architecture/0010-vps-provisioning-via-opentofu.md) for why this
exists and [ADR-0005](../../docs/architecture/0005-hosting-provider-and-sizing.md) for
the sizing decision.

**Scope boundary:** this stops at the OS. Hardening, Docker, Caddy, and Nextcloud AIO are
Ansible's job (ADR-0001), not OpenTofu's.

## Prerequisites
- [OpenTofu](https://opentofu.org/docs/intro/install/) >= 1.6
- A Hetzner Cloud project + API token (Console → your project → Security → API Tokens →
  generate one scoped to this project, read+write). Store it in the Proton Pass vault
  (SEC-2) once created.
- An SSH key pair already generated locally (`ssh-keygen -t ed25519`) — only the
  `.pub` file is read by this config.

## Usage

```sh
cd infra/opentofu
cp terraform.tfvars.example terraform.tfvars   # edit as needed; this file is gitignored
```

Set `admin_ipv4_cidrs`/`admin_ipv6_cidrs` in `terraform.tfvars` to your known IP(s) —
these are required (no open default), so `plan`/`apply` will fail until you've made an
explicit choice. Use `[]` for whichever family you're not restricting.

```sh
export HCLOUD_TOKEN="<your Hetzner API token>" # never put this in a .tfvars file

tofu init
tofu plan
tofu apply
```

### Sourcing `HCLOUD_TOKEN` from Proton Pass

The token should live only in the vault (SEC-2), not in shell history or a dotfile. The
[Proton Pass CLI](https://protonpass.github.io/pass-cli/) (`pass-cli`, included in Pass
Plus — see [ADR-0007](../../docs/architecture/0007-secrets-management.md)) resolves a
`pass://vault/item/field` reference and injects it into a child process's environment,
so the plaintext token never touches disk or your shell:

```sh
curl -fsSL https://proton.me/download/pass-cli/install.sh | bash
pass-cli login
pass-cli list   # find the exact vault/item path you saved the token under

HCLOUD_TOKEN="pass://<vault-name>/<item-name>/<field>" \
  pass-cli run -- tofu -chdir=infra/opentofu apply
```

On success:

```sh
tofu output server_ipv4
tofu output server_ipv6
```

Feed these into the Ansible inventory (INFRA-3) and, once the domain is registered
(GOV-2), into the A/AAAA DNS records.

## State
State is kept **local** (`terraform.tfstate`, gitignored) — appropriate for a single-box,
single-admin setup. It holds resource IDs/metadata, not secrets. If a second admin needs
to run `tofu apply` (see ADR-0009), move to a shared backend first rather than passing
the local state file around.

## Destroying
`tofu destroy` deletes the server. This is a genuinely destructive, hard-to-reverse
action — confirm you have a current, verified backup (BKP-4) before ever running it
against a production box. `hcloud_server.this` carries `lifecycle { prevent_destroy = true }`
as a guardrail against a fat-fingered `destroy`; remove that block locally (don't commit
the removal) if you genuinely intend to destroy the server.
