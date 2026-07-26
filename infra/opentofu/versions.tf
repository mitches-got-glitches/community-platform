terraform {
  required_version = ">= 1.6.0"

  required_providers {
    hcloud = {
      source  = "hetznercloud/hcloud"
      version = "~> 1.48"
    }
  }
}

provider "hcloud" {
  # Token is read from the HCLOUD_TOKEN environment variable — deliberately not
  # wired to a Terraform variable, so the provider's built-in env-var lookup
  # applies (see README.md).
}
