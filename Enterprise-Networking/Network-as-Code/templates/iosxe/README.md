# IOS-XE Network as Code templates

YAML for the IOS-XE data model at <https://netascode.cisco.com/docs/data_models/iosxe/>. The schema is `iosxe` in [netascode/schema](https://github.com/netascode/schema/blob/7334e341147fabf81071f18b0286e7deac47d9ab/schema.json) commit `7334e341147fabf81071f18b0286e7deac47d9ab` (2026-10-22).

Validated with Python `jsonschema` (`Draft202012Validator`) against that file. `nac-validate` was not used: the published artifact is JSON Schema, and `nac-validate` 2.0.0 reads Yamale only. See [../README.md](../README.md).

## Terraform

| | |
| --- | --- |
| Module | `netascode/nac-iosxe/iosxe` 1.0.0 |
| Provider | `CiscoDevNet/iosxe` 1.0.0 (the module allows `>= 1.0.0`) |
| Utils | `netascode/utils` `>= 2.0.2, < 3.0.0` |
| Terraform | `>= 1.9.0` |

The working root is [`../../iosxe/`](../../iosxe/). It reads `iosxe/data/`, not this directory. Copy a template section into that `data/` tree (or point a separate root at the files you copied). Set `IOSXE_USERNAME` and `IOSXE_PASSWORD`. Do not put those values in YAML.

```bash
cd Enterprise-Networking/Network-as-Code/iosxe
export IOSXE_USERNAME="admin"
export IOSXE_PASSWORD="replace-me"
terraform init
terraform plan
```

`nac-iosxe` 1.0.0 builds the provider device list from the YAML `devices` entries and reads the username and password from the environment.

## Layout

77 files.

| Directory | Contents |
| --- | --- |
| `entity/` | `global`, `devices`, `device_groups`, `templates`, and the interface-group object, with `configuration` left empty |
| `device/` | One file per top-level `devices[].configuration` key other than interfaces and routing |
| `interface/` | Ethernet, loopback, VLAN, NVE, port-channel, tunnel, BDI, interface range, and the interface-group configuration |
| `routing/` | BGP, EIGRP, IS-IS, OSPF, static routes |

`global`, `device_groups`, and `templates` use the same `configuration` schema as `devices`. It is written out only under `device/`, `interface/`, and `routing/`.

## Module behavior to keep when you copy a template

Interface ids here are the form the schema accepts, such as `0/0`. `nac-iosxe` 1.0.0 still expects the `"$string "` prefix on non-integer interface ids for resources that strip it. The schema pattern does not allow that space, so the prefix is not in these files. Add it when you copy an interface id into `iosxe/data/`, except OSPF `non_passive_interfaces.interface_id`, which `nac-iosxe` 1.0.0 copies without stripping the prefix.

## Schema sections with no docs page

`device/bridge_domains.nac.yaml`, `device/ipv6_pim.nac.yaml`, `device/vlan.nac.yaml`, `interface/interface-group.nac.yaml`, and `interface/ranges.nac.yaml`. The interface VLAN page is cited from `interface/vlans.nac.yaml`, which is the interface list, not the device `vlan` object.
