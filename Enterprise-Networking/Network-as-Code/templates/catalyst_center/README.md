# Catalyst Center Network as Code templates

YAML for the Catalyst Center data model at <https://netascode.cisco.com/docs/data_models/catalyst_center/>, including the SD-Access fabric. The schema is `catalyst_center` in [netascode/schema](https://github.com/netascode/schema/blob/7334e341147fabf81071f18b0286e7deac47d9ab/schema.json) commit `7334e341147fabf81071f18b0286e7deac47d9ab` (2026-10-22).

Validated with Python `jsonschema` (`Draft202012Validator`) against that file. `nac-validate` was not used: the published artifact is JSON Schema, and `nac-validate` 2.0.0 reads Yamale only. See [../README.md](../README.md).

## Terraform

| | |
| --- | --- |
| Module | `netascode/nac-catalystcenter/catalystcenter` 0.5.1 |
| Provider | `CiscoDevNet/catalystcenter` `~> 0.6.5` |
| Utils | `netascode/utils` `>= 2.0.0` |
| Also required by the module | `hashicorp/local` `>= 2.3.0`, `hashicorp/time` `>= 0.12.1` |
| Terraform | `>= 1.15.0` |

`provider_meta` on that tag is `NAC/0.5.1`. Give this module its own root. Point `yaml_files` or `yaml_directories` at the files you copied. The provider reads `CC_URL`, `CC_USERNAME`, and `CC_PASSWORD`.

```bash
export CC_URL="https://catalyst-center.example.com"
export CC_USERNAME="admin"
export CC_PASSWORD="replace-me"
terraform init
terraform plan
```

There is no Catalyst Center Terraform root in this repository yet. Fabric CLI notes stay under [`../../../SD-Access/`](../../../SD-Access/).

## Layout

70 files.

| Directory | Contents |
| --- | --- |
| `sites/` | Areas, buildings, floors |
| `inventory/` | Devices, discovery, tags |
| `network_settings/` | Network, IP pools, telemetry, AAA servers, device credentials |
| `network_profiles/` | Switching and wireless profiles |
| `wireless/` | SSIDs, RF, AP, power, interfaces, anchors, and related wireless objects |
| `fabric/` | L3 virtual networks, extranet policies, transits, fabric sites (including zones and anycast gateways), border devices |
| `lan_automation/` | Devices and links |
| `templates/` | Projects (onboarding and day-N) and tags |
| root | `authentication_templates.nac.yaml`, `feature_templates.nac.yaml` |

Device-credential and server-secret attributes are placeholders such as `<SECRET>`. Do not commit real Catalyst Center credentials or ISE shared secrets.
