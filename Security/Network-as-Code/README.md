# Security Network as Code

YAML data models that Terraform pushes to Cisco Secure Firewall Management Center (FMC) and Cisco Identity Services Engine (ISE). These files are templates: copy the blocks you need and delete the rest before `terraform plan` against a real system. Credentials come from environment variables only. Do not commit filled-in secrets, Terraform state, or `.terraform/` directories.

## Folder index

| Folder | Purpose |
| --- | --- |
| [templates/fmc](templates/fmc/) | FMC data model templates (module `netascode/nac-fmc/fmc` 0.1.3, provider `CiscoDevNet/fmc` 2.6.1). See the [FMC README](templates/fmc/README.md). |
| [templates/ise](templates/ise/) | ISE data model templates (module `netascode/nac-ise/ise` 1.1.0, provider `CiscoDevNet/ise` 0.5.2). See the [ISE README](templates/ise/README.md). |

Each technology is its own Terraform root. Run `terraform init` and `terraform validate` from that folder, and `python3 scripts/validate_schema.py` to check the YAML against the published netascode/schema JSON Schema. Details, environment variables, and coverage tables are in the technology READMEs.
