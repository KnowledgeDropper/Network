# Network as Code templates

Reference YAML for the five enterprise-networking data models on [netascode.cisco.com](https://netascode.cisco.com/docs/data_models/). Each file is one section of the published schema, with placeholders and comments for mandatory attributes, ranges, and allowed values.

These files are not a configuration you apply as a set. They list every attribute the schema allows, including attributes a device rejects together. Copy the sections you need into a Terraform root's `data/` directory, delete the attributes that device will not use, and replace every placeholder. The working roots `../iosxe/` and `../iosxr/` keep reading `data/` only.

| Directory | Model | Files | Module |
| --- | --- | --- | --- |
| [iosxe](iosxe/) | IOS-XE | 77 | `netascode/nac-iosxe/iosxe` 1.0.0 |
| [iosxr](iosxr/) | IOS-XR | 74 | `netascode/nac-iosxr/iosxr` 0.1.1 |
| [sdwan](sdwan/) | Catalyst SD-WAN | 297 | `netascode/nac-sdwan/sdwan` 1.5.0 |
| [catalyst_center](catalyst_center/) | Catalyst Center (SD-Access) | 70 | `netascode/nac-catalystcenter/catalystcenter` 0.5.1 |
| [meraki](meraki/) | Meraki | 194 | `netascode/nac-meraki/meraki` 0.12.0 |

## Schema and validator

Published schema: [netascode/schema `schema.json`](https://github.com/netascode/schema/blob/7334e341147fabf81071f18b0286e7deac47d9ab/schema.json) at commit `7334e341147fabf81071f18b0286e7deac47d9ab` (2026-10-22). JSON Schema draft 2020-12.

`nac-validate` 2.0.0 reads Yamale schemas only. That repository ships `schema.json` and no Yamale schema, and the Terraform module tags above do not ship `nac/schema.yaml`. All five models were validated with Python `jsonschema` 4.26.0, `Draft202012Validator`, against that file. `yamllint` was run with [`.yamllint.yml`](.yamllint.yml) in this directory.

Each file was checked on its own. A document that contains only that model's top-level key is valid. Ancestor keys the schema marks required are filled in so the file still validates alone.

## Placeholders

`<HOSTNAME>`, `<NAME>`, `<DESCRIPTION>`, `<SECRET>`, `<PASSWORD>`, `<VARIABLE>`, `10.0.0.1`, `10.0.0.0/24`, `example.com`, `admin@example.com`, and `https://example.com` stand in for site values. Enums use a value the schema allows. Replace them before apply. Do not commit real secrets. Credentials stay in environment variables; see each technology README.

## How the large models are split

IOS-XE and IOS-XR use the same `configuration` object under `global`, `device_groups`, `devices`, and `templates`. That object is written out once, under `device/`, `interface/`, and `routing/`. The entity files keep `configuration: {}` and point at those files. `interface/interface-group.nac.yaml` is a different, interface-level object and is expanded on its own.

Meraki `templates.networks[].configuration` and `templates.devices[].configuration` match the live network and device objects aside from `default` metadata. Those attributes are expanded under `domains/`. The two files in `meraki/templates/` repeat only the required keys.

SD-WAN, Catalyst Center, and Meraki are split on the schema's section objects, including array items that are themselves section objects. A `common.nac.yaml` file holds the scalar siblings of a section that was split.

## Published schema defects

Six fields cannot be satisfied. The schema declares one type and an `enum` of another type, and draft 2020-12 rejects every value. The templates keep the documented allowed value and say so in a comment. `jsonschema` reports these and no other errors:

| Model | Path | Declared type | Allowed value in the template |
| --- | --- | --- | --- |
| SD-WAN | `centralized_policies.definitions.data_policy.traffic_data[].sequences[].actions.cflowd` | integer | `true` |
| SD-WAN | `...actions.sig.enabled` | integer | `true` |
| Meraki | `...appliance.rf_profiles[].two_four_ghz_settings.min_bitrate` | string | `1` |
| Meraki | `...wireless.rf_profiles[].two_four_ghz_settings.min_bitrate` | string | `1` |
| Meraki | `...wireless.rf_profiles[].per_ssid_settings[].min_bitrate` | string | `1` |
| Meraki | `...wireless.ssids[].min_bitrate` | string | `11` (the schema default) |

The same Meraki `min_bitrate` nodes also exist under `templates.networks[].configuration`, which these templates do not expand.

## Docs coverage

Every page under `/docs/data_models/{iosxe,iosxr,sdwan,catalyst_center,meraki}/` in the docs nav is cited in at least one file header, except the narrative pages `overview`, `features`, and `renaming_resources`. Some schema sections have no page of their own. Those headers say so. The IOS-XE and IOS-XR lists are in those directories' READMEs. Nested SD-WAN, Catalyst Center, and Meraki files in that situation are child objects whose attributes are documented on the parent page linked from a sibling file.
