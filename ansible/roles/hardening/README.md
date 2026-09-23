# hardening (reserved)

Empty on purpose. Host-hardening specifics — `unattended-upgrades`, UFW, `fail2ban` —
belong to INFRA-4 (#13) and are governed by
[ADR-0008](../../../docs/architecture/0008-operational-baseline.md). This directory
just reserves the role's place in the `roles/` layout; it is not wired into
[`../../site.yml`](../../site.yml) yet, so it plays no part in `ansible-playbook --check`.

When INFRA-4 lands, add `tasks/main.yml` here and append `hardening` to the role list
in `site.yml`.
