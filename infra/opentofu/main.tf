resource "hcloud_ssh_key" "admin" {
  name       = "${var.server_name}-admin"
  public_key = file(var.ssh_public_key_path)
}

resource "hcloud_firewall" "web_and_ssh" {
  name = "${var.server_name}-fw"

  rule {
    direction  = "in"
    protocol   = "tcp"
    port       = "22"
    source_ips = concat(var.admin_ipv4_cidrs, var.admin_ipv6_cidrs)
  }

  rule {
    direction  = "in"
    protocol   = "tcp"
    port       = "80"
    source_ips = ["0.0.0.0/0", "::/0"]
  }

  rule {
    direction  = "in"
    protocol   = "tcp"
    port       = "443"
    source_ips = ["0.0.0.0/0", "::/0"]
  }
}

resource "hcloud_server" "this" {
  name         = var.server_name
  server_type  = var.server_type
  location     = var.location
  image        = var.image
  ssh_keys     = [hcloud_ssh_key.admin.id]
  firewall_ids = [hcloud_firewall.web_and_ssh.id]

  public_net {
    ipv4_enabled = true
    ipv6_enabled = true
  }
}
