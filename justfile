# Recurring commands for this repo. Run `just --list` to see what's available.
# Add new recurring workflows here rather than leaving them as copy-paste
# snippets in docs.

vault_name := "BAFZ Vault"
hcloud_token_ref := "pass://" + vault_name + "/Hetzner API Key/password"
nc_item := "Claude Nextcloud App"
nc_url_ref := "pass://" + vault_name + "/" + nc_item + "/urls"
nc_user_ref := "pass://" + vault_name + "/" + nc_item + "/username"
nc_pass_ref := "pass://" + vault_name + "/" + nc_item + "/password"
nc_env := 'NC_URL="' + nc_url_ref + '" NC_USER="' + nc_user_ref + '" NC_PASS="' + nc_pass_ref + '"'

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

# Smoke-test the Nextcloud API credential and show the running version
nc-check:
    {{nc_env}} pass-cli run -- python3 scripts/nc.py check

# List Nextcloud accounts, display names, emails and groups (for the access register)
nc-users:
    {{nc_env}} pass-cli run -- python3 scripts/nc.py users

# Create an account and send its activation email (see the "How to add a user" admin guide)
nc-user-add login email:
    {{nc_env}} pass-cli run -- python3 scripts/nc.py user-add {{login}} {{email}}

# Pull every wiki page to local markdown — own-copy backup and migration insurance (ADR-0006).
# Output contains member content: gitignored, never committed to this public repo.
nc-wiki-export dir="wiki-export":
    {{nc_env}} pass-cli run -- python3 scripts/nc.py wiki-export {{dir}}

# List wiki pages still holding a 🎬 screen-recording placeholder
nc-wiki-todo:
    {{nc_env}} pass-cli run -- python3 scripts/nc.py wiki-todo
