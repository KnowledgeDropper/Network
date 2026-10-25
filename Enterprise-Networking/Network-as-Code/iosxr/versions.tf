terraform {
  required_version = ">= 1.8.0"

  required_providers {
    # nac-iosxr 0.1.1 requires this provider version exactly.
    iosxr = {
      source  = "CiscoDevNet/iosxr"
      version = "0.7.1"
    }
  }
}
