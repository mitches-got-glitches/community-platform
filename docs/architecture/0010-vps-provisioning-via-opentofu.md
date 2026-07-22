# ADR-0010: VPS provisioning via OpenTofu

- **Status:** Accepted
- **Date:** 2026-07-22
- **Deciders:** Technical admin

## Context
[ADR-0001](0001-nextcloud-backbone-and-deployment.md) decided that an Ansible playbook
configures Nextcloud AIO on top of "a bare VPS" — but it never decided how that bare VPS
itself gets created. Left as-is, that step defaults to clicking through the Hetzner Cloud
Console by hand: undocumented, unreproducible, and the one part of the stack that would
not survive the admin (or a rebuild) without tribal knowledge. That is directly at odds
with the "code-first / reproducible" hard constraint in `CLAUDE.md`.

INFRA-2 (provision the VPS) and INFRA-3 (the Ansible repo skeleton / "IaC spine") are the
first two build tasks under Epic A, so this gap needed closing before either could start.

## Decision
Use **OpenTofu** with the `hetznercloud/hcloud` provider to declare the pieces that exist
*below* the OS Ansible configures:
- the **Hetzner CAX31 server** (ADR-0005), in an EU region (DE/FI)
- an **`hcloud_ssh_key`** resource (public key only — the private key never touches the repo
  or Terraform state)
- an **`hcloud_firewall`** allowing only 22/80/443, attached to the server (defence in depth
  ahead of the host-level UFW rules INFRA-4 configures)

OpenTofu outputs the server's IPv4/IPv6, which feeds the Ansible inventory (INFRA-3).
Everything from the OS up — hardening, Docker, Caddy, AIO — remains Ansible's job, per
ADR-0001. Nothing in that decision changes.

## Alternatives considered
- **Manual creation via Hetzner Cloud Console:** rejected — the gap this ADR exists to close;
  fails "code-first / reproducible" and worsens the bus-factor story (see ADR-0009).
- **Terraform (HashiCorp):** functionally equivalent, same provider ecosystem. Rejected in
  favour of OpenTofu, which is fully open-source (Linux Foundation, MPL-2.0) rather than
  HashiCorp's BSL — a better fit for a project whose stated priority is sovereignty and
  open-source tooling, at no practical cost (OpenTofu is a drop-in-compatible fork; same
  HCL syntax, same `hcloud` provider).
- **Ansible alone (`hcloud` Ansible modules) for VPS creation too:** viable, but blurs the
  ADR-0001 split between "provisioning the box" and "configuring the box," and Ansible's
  imperative module-per-run model is a weaker fit for declarative infrastructure than
  OpenTofu's plan/apply state model.

## Consequences
- **Positive:** VPS creation is now version-controlled and reproducible — closes the gap
  ADR-0001 left open; a from-scratch rebuild starts with `tofu apply`, not console clicks.
- **Negative / accepted:** one more tool for a solo admin to know. Mitigated by the small
  surface area here — a handful of resources (server, SSH key, firewall), not a general
  Hetzner estate.
- OpenTofu state contains resource IDs and metadata but **not** the Hetzner API token or
  the SSH private key. State is kept local (not committed) for a single-box, single-admin
  setup; the Hetzner API token lives in the Proton Pass vault (SEC-2), passed via the
  `HCLOUD_TOKEN` environment variable, never written to a committed `.tfvars` file.

## Conditions / follow-ups
- INFRA-3 (Ansible inventory) consumes the `server_ipv4` / `server_ipv6` outputs.
- If a second admin needs to run `tofu apply`, state must move to a shared backend
  (e.g. an encrypted object-storage backend) rather than staying local-only — revisit
  alongside ADR-0009's second-admin onboarding.
