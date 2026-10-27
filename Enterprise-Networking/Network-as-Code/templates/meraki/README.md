# Meraki Network as Code templates

YAML for the Meraki data model at <https://netascode.cisco.com/docs/data_models/meraki/>. The schema is `meraki` in [netascode/schema](https://github.com/netascode/schema/blob/7334e341147fabf81071f18b0286e7deac47d9ab/schema.json) commit `7334e341147fabf81071f18b0286e7deac47d9ab` (2026-10-22).

Validated with Python `jsonschema` (`Draft202012Validator`) against that file. `nac-validate` was not used: the published artifact is JSON Schema, and `nac-validate` 2.0.0 reads Yamale only. Four `min_bitrate` fields fail that check because the published schema types them as string and lists numeric enums. See [../README.md](../README.md).

## Terraform

| | |
| --- | --- |
| Module | `netascode/nac-meraki/meraki` 0.12.0 |
| Provider | `CiscoDevNet/meraki` `>= 1.14.1` |
| Terraform | `>= 1.9.0` |

Use a root of its own and point `yaml_directories` or `yaml_files` at the files you copied. The provider reads `MERAKI_API_KEY`. Do not put the API key in YAML.

```bash
export MERAKI_API_KEY="replace-me"
terraform init
terraform plan
```

## Layout

194 files.

`domains/` is the live hierarchy: administrator, then `organizations/` (appliance, switch, wireless, networks, and the organization-level objects). Network appliance, switch, and wireless settings are nested under `domains/organizations/networks/`.

`templates/networks.nac.yaml` and `templates/devices.nac.yaml` are the reusable template objects. Their `configuration` blocks repeat only required keys. The attribute list matches the live network and device model and is expanded under `domains/`.

## Published schema defects

These `min_bitrate` keys are type string with a numeric enum. The template uses the documented number (`11` on SSIDs, where that is the schema default, and `1` on the other three):

- `domains/organizations/networks/appliance/rf_profiles/two_four_ghz_settings.nac.yaml`
- `domains/organizations/networks/wireless/rf_profiles/two_four_ghz_settings.nac.yaml`
- `domains/organizations/networks/wireless/rf_profiles/per_ssid_settings.nac.yaml`
- `domains/organizations/networks/wireless/ssids.nac.yaml`

Five GHz and six GHz `min_bitrate` attributes are integers with numeric enums, and those values validate.
