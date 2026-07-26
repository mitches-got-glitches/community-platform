# Recurring commands for this repo. Run `just --list` to see what's available.
# Add new recurring workflows here rather than leaving them as copy-paste
# snippets in docs.

vault_name := "BAFZ Vault"
hcloud_token_ref := "pass://" + vault_name + "/Hetzner API Key/password"

# Preview infrastructure changes (see infra/opentofu/README.md)
tofu-plan:
    HCLOUD_TOKEN="{{hcloud_token_ref}}" pass-cli run -- tofu -chdir=infra/opentofu plan

# Apply infrastructure changes (see infra/opentofu/README.md) — review the plan first
tofu-apply:
    HCLOUD_TOKEN="{{hcloud_token_ref}}" pass-cli run -- tofu -chdir=infra/opentofu apply

# Audit who has vault access and list its items (see docs/runbooks/pass-family-admin-onboarding.md)
vault-members:
    pass-cli vault list
    pass-cli item list --vault-name "{{vault_name}}"

# Dry-run the Ansible playbook against the production inventory (see ansible/README.md)
ansible-check:
    cd ansible && uv run ansible-playbook site.yml --check

# Apply the Ansible playbook against the production inventory (see ansible/README.md)
ansible-apply:
    cd ansible && uv run ansible-playbook site.yml
