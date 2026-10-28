# Catalyst SD-WAN Network as Code templates

YAML for the Catalyst SD-WAN data model at <https://netascode.cisco.com/docs/data_models/sdwan/>. The schema is `sdwan` in [netascode/schema](https://github.com/netascode/schema/blob/7334e341147fabf81071f18b0286e7deac47d9ab/schema.json) commit `7334e341147fabf81071f18b0286e7deac47d9ab` (2026-10-22).

Validated with Python `jsonschema` (`Draft202012Validator`) against that file. `nac-validate` was not used: the published artifact is JSON Schema, and `nac-validate` 2.0.0 reads Yamale only. See [../README.md](../README.md).

## Terraform

| | |
| --- | --- |
| Module | `netascode/nac-sdwan/sdwan` 1.5.0 |
| Provider | `CiscoDevNet/sdwan` `~> 0.11.5` |
| Utils | `netascode/utils` `>= 2.0.1, < 3.0.0` |
| Terraform | `>= 1.8.0` |

Use a root of its own. The utils constraint matches IOS-XE and conflicts with IOS-XR. Point `yaml_directories` or `yaml_files` at the files you copied, not at this whole tree. The provider reads `SDWAN_URL`, `SDWAN_USERNAME`, and `SDWAN_PASSWORD` (or `SDWAN_API_TOKEN`).

```bash
export SDWAN_URL="https://sdwan-manager.example.com"
export SDWAN_USERNAME="admin"
export SDWAN_PASSWORD="replace-me"
terraform init
terraform plan
```

There is no SD-WAN Terraform root in this repository yet. CLI templates for cEdge and vEdge stay under [`../../../SD-WAN/`](../../../SD-WAN/).

## Layout

297 files. Top-level keys that are a single object or a short list sit in the directory root (`application_catalog.nac.yaml`, `common.nac.yaml`, `configuration_groups.nac.yaml`, `edge_device_templates.nac.yaml`, `multi_region_fabric.nac.yaml`, `policy_groups.nac.yaml`, `settings.nac.yaml`, `sites.nac.yaml`, `topology_groups.nac.yaml`). The rest are split by section:

| Directory | Contents |
| --- | --- |
| `edge_feature_templates/` | Classic feature templates, one file (or a small directory) per template list |
| `policy_objects/` | Classic policy objects |
| `localized_policies/` | Definitions and the feature policy |
| `centralized_policies/` | Topology, data, and control definitions, plus feature policies |
| `security_policies/` | Intrusion prevention and zone-based firewall |
| `feature_profiles/` | UX 2.0 profiles: system, transport, service, policy object, application priority, topology, SSE, other, CLI, and NGFW |
| `network_hierarchy/` | Regions, sites, groups, and collectors |

`common.nac.yaml` next to a split section holds that object's scalar keys. `settings.nac.yaml` includes cloud-provider credential attributes; those values are placeholders.

## Published schema defect

`centralized_policies/definitions/data_policy/traffic_data.nac.yaml` sets `sequences[].actions.cflowd` and `sequences[].actions.sig.enabled` to `true`. The schema types both as integer and allows only boolean `true`, so no value passes draft 2020-12. The comment on each key records that.
