terraform {
  # netascode/nac-ise/ise 1.1.0 requires >= 1.11.0 (write-only *_wo secret arguments in CiscoDevNet/ise).
  required_version = ">= 1.11.0"

  required_providers {
    ise = {
      source = "CiscoDevNet/ise"
      # Latest on registry.terraform.io (verified 2026-10-27): 0.5.2 (published 2026-10-23).
      # Module 1.1.0 requires "~> 0.5.0".
      version = "0.5.2"
    }
    utils = {
      source  = "netascode/utils"
      version = "2.0.0" # module 1.1.0 pins exactly 2.0.0
    }
    local = {
      source  = "hashicorp/local"
      version = ">= 2.3.0"
    }
    time = {
      source  = "hashicorp/time"
      version = ">= 0.10.0"
    }
  }
}
