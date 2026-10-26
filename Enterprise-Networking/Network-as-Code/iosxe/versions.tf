terraform {
  required_version = ">= 1.9.0"

  required_providers {
    # Pinned to the release nac-iosxe 1.0.0 was tested with.
    # The module constraint is >= 1.0.0; leaving it open pulls a newer
    # provider and can drift from the YAML schema used here.
    iosxe = {
      source  = "CiscoDevNet/iosxe"
      version = "1.0.0"
    }
  }
}
