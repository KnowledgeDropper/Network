# IOS-XR Network as Code templates

YAML for the IOS-XR data model at <https://netascode.cisco.com/docs/data_models/iosxr/>. The schema is `iosxr` in [netascode/schema](https://github.com/netascode/schema/blob/7334e341147fabf81071f18b0286e7deac47d9ab/schema.json) commit `7334e341147fabf81071f18b0286e7deac47d9ab` (2026-10-22).

Validated with Python `jsonschema` (`Draft202012Validator`) against that file. `nac-validate` was not used: the published artifact is JSON Schema, and `nac-validate` 2.0.0 reads Yamale only. See [../README.md](../README.md).

## Terraform

| | |
| --- | --- |
| Module | `netascode/nac-iosxr/iosxr` 0.1.1 |
| Provider | `CiscoDevNet/iosxr` 0.7.1 |
| Utils | `netascode/utils` `= 1.1.0-beta5` |
| Terraform | `>= 1.8.0` |

The utils pin conflicts with IOS-XE, so this stays a separate root. The working root is [`../../iosxr/`](../../iosxr/) and reads `iosxr/data/` only. Copy the sections you need into that `data/` tree. Set `IOSXR_USERNAME` and `IOSXR_PASSWORD`.

```bash
cd Enterprise-Networking/Network-as-Code/iosxr
export IOSXR_USERNAME="admin"
export IOSXR_PASSWORD="replace-me"
terraform init
terraform plan
```

## Layout

74 files.

| Directory | Contents |
| --- | --- |
| `entity/` | `global`, `devices`, `device_groups`, `templates`, and the interface-group object, with `configuration` left empty |
| `device/` | One file per top-level `devices[].configuration` key other than interfaces and routing |
| `interface/` | Ethernet, bundle-ethernet, BVI, loopback, tunnel-ip, tunnel-te, and the interface-group configuration |
| `routing/` | BGP, IS-IS, OSPF, static routes |

`global`, `device_groups`, and `templates` share the `devices[].configuration` schema. That object is written out only under `device/`, `interface/`, and `routing/`. `gnmi` is an open map, so the template has one example key.

## Module behavior to keep when you copy a template

`nac-iosxr` 0.1.1 joins every line of a `cli_templates` entry with spaces before `iosxr_cli`. Keep each template a single command. Telnet `max-servers 0` cannot be set through the `telnet` resource on provider 0.7.1 (the leaves accept 1–100); the working root sends that through a CLI template. TACACS key leaves want type 6 or type 7 material, not cleartext. SNMPv3 passwords on the default-encryption leaf allow only `[0-9a-zA-Z]`.

Interface ids here are the form the schema accepts (`0/0`, subinterface `0/0.1`). Where the module strips a `"$string "` prefix, add that prefix in `iosxr/data/`. The schema rejects the space, so these templates do not include it.

## Schema sections with no docs page

`device/aaa.nac.yaml`, `device/as_format.nac.yaml`, `device/as_path_sets.nac.yaml`, `device/mpls_ldp.nac.yaml`, `device/radius_server.nac.yaml`, `device/tacacs_source_interface.nac.yaml`, `device/taskgroups.nac.yaml`, `device/tcp.nac.yaml`, `device/usergroups.nac.yaml`, `device/usernames.nac.yaml`, and `interface/interface-group.nac.yaml`.
