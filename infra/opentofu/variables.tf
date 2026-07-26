variable "server_name" {
  description = "Name of the Hetzner Cloud server."
  type        = string
  default     = "community-platform"
}

variable "server_type" {
  description = "Hetzner server type. ADR-0005: CAX31 (ARM, 8 vCPU/16GB). Falls back to CPX31 (x86) only if an AIO add-on lacks an arm64 image."
  type        = string
  default     = "cax31"
}

variable "location" {
  description = "Hetzner datacentre location. ADR-0005: an EU region (DE or FI)."
  type        = string
  default     = "fsn1" # Falkenstein, DE

  validation {
    condition     = contains(["fsn1", "nbg1", "hel1"], var.location)
    error_message = "Location must be an EU Hetzner datacentre: fsn1 (Falkenstein), nbg1 (Nuremberg), or hel1 (Helsinki)."
  }
}

variable "image" {
  description = "Base OS image for the server."
  type        = string
  default     = "ubuntu-24.04"
}

variable "ssh_public_key_path" {
  description = "Path to the admin's SSH public key file. Only the public key is read — never the private key."
  type        = string
  default     = "~/.ssh/id_ed25519.pub"
}

variable "admin_ipv4_cidrs" {
  description = "IPv4 CIDR blocks allowed to reach SSH (port 22). Required — no open default, so a plan/apply forces an explicit choice instead of silently exposing SSH to the internet. Set to [] if not restricting over IPv4."
  type        = list(string)
}

variable "admin_ipv6_cidrs" {
  description = "IPv6 CIDR blocks allowed to reach SSH (port 22). Required — no open default; see admin_ipv4_cidrs. Set to [] if not restricting over IPv6."
  type        = list(string)
}
