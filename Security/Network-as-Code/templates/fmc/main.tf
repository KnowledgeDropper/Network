# -----------------------------------------------------------------------------
# Cisco Secure Firewall Management Center (FMC) - Network-as-Code template library
#
# All intent lives in YAML under data/ (optional overrides under defaults/).
# Terraform only wires the NaC module to the CiscoDevNet/fmc provider.
# The data/ files are TEMPLATES that exercise every attribute of the data model;
# trim them to what you need before planning against a real FMC.
# -----------------------------------------------------------------------------

# Credentials are NEVER stored here. The provider reads them from the environment:
#   Self-hosted FMC : FMC_URL, FMC_USERNAME, FMC_PASSWORD
#   cdFMC / SCC FM  : FMC_URL, FMC_TOKEN
#   Optional        : FMC_INSECURE (provider default true!), FMC_RETRIES, FMC_REQTIMEOUT
# Secrets inside the YAML use `!env VAR` tags (resolved by netascode/utils yaml_merge) -
# see README.md for the list of FMC_* variables referenced by the templates.
provider "fmc" {
  # Intentionally empty - every attribute is sourced from FMC_* env vars.
}

module "fmc" {
  source  = "netascode/nac-fmc/fmc"
  version = "0.1.3" # latest on registry.terraform.io (verified 2026-10-27)

  # Every *.yaml / *.yml in these directories is deep-merged into one model.
  # Top-level keys used: fmc (managed config) and existing (read-only lookups).
  yaml_directories = ["data"]

  # Module default true: trigger FTD deployments for managed devices after changes.
  manage_deployment = true

  # write_default_values_file = "defaults_effective.yaml"
}

output "model" {
  description = "Fully merged NaC model as seen by the module (useful for troubleshooting)."
  value       = module.fmc.model
  sensitive   = true
}
