output "server_ipv4" {
  description = "Public IPv4 address of the server. Feeds the Ansible inventory (INFRA-3) and DNS A record (GOV-2)."
  value       = hcloud_server.this.ipv4_address
}

output "server_ipv6" {
  description = "Public IPv6 address of the server. Feeds the Ansible inventory (INFRA-3) and DNS AAAA record (GOV-2)."
  value       = hcloud_server.this.ipv6_address
}

output "server_id" {
  description = "Hetzner Cloud server ID."
  value       = hcloud_server.this.id
}
