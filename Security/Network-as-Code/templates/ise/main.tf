# -----------------------------------------------------------------------------
# Cisco Identity Services Engine (ISE) - Network-as-Code template library
#
# All intent lives in YAML under data/. Terraform only wires the NaC module to
# the CiscoDevNet/ise provider. The data/ files are TEMPLATES that exercise every
# attribute of the data model; trim them before planning against a real ISE.
# -----------------------------------------------------------------------------

# Credentials are NEVER stored here. The provider reads them from the environment:
#   ISE_URL, ISE_USERNAME, ISE_PASSWORD
#   Optional: ISE_INSECURE (provider default true!), ISE_RETRIES, ISE_REQUEST_TIMEOUT
# ERS + Open API must be enabled on ISE. Secrets inside the YAML use `!env VAR`
# tags (resolved by netascode/utils yaml_merge) - see README.md for the ISE_* list.
provider "ise" {
  # Intentionally empty - every attribute is sourced from ISE_* env vars.
}

module "ise" {
  source  = "netascode/nac-ise/ise"
  version = "1.1.0" # latest on registry.terraform.io (verified 2026-10-27)

  yaml_directories = ["data"]

  # write_default_values_file = "defaults_effective.yaml"
}

output "model" {
  description = "Fully merged NaC model as seen by the module (useful for troubleshooting)."
  value       = module.ise.model
  sensitive   = true
}
