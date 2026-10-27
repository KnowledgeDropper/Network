terraform {
  # netascode/nac-fmc/fmc 0.1.3 uses provider-defined functions from netascode/utils -> Terraform >= 1.8.0.
  required_version = ">= 1.8.0"

  required_providers {
    fmc = {
      source = "CiscoDevNet/fmc"
      # Latest on registry.terraform.io (verified 2026-10-27): 2.6.1 (published 2026-09-23).
      # Module 0.1.3 accepts ">= 2.3.0, < 3.0.0".
      version = "2.6.1"
    }
    utils = {
      source  = "netascode/utils"
      version = ">= 2.0.0, < 3.0.0" # module constraint; 2.1.0-beta2 exists but pre-releases are not selected by ranges
    }
    local = {
      source  = "hashicorp/local"
      version = ">= 2.3.0, < 3.0.0"
    }
  }
}
