# Network as Code

YAML data that Terraform pushes to Cisco IOS-XE and IOS-XR. Edit the data files, then plan and apply. The CLI templates under `IOS-XE/` and `IOS-XR/` stay the paste-oriented baseline. This folder is the same baseline expressed in Cisco's Network as Code model.

Addresses are documentation prefixes from RFC 5737 (`192.0.2.0/24`, `198.51.100.0/24`). Secret fields are placeholders such as `<TACACS_KEY>`. Replace them before apply. Do not commit the filled-in values.

## Workflow

IOS-XE and IOS-XR are separate Terraform roots. Run the commands in the root for the platform you are changing.

```bash
cd Enterprise-Networking/Network-as-Code/iosxe
export IOSXE_USERNAME="admin"
export IOSXE_PASSWORD="replace-me"
terraform init
terraform plan
terraform apply
```

```bash
cd Enterprise-Networking/Network-as-Code/iosxr
export IOSXR_USERNAME="admin"
export IOSXR_PASSWORD="replace-me"
terraform init
terraform plan
terraform apply
```

`terraform plan` shows the device change set. `terraform apply` pushes it. Neither command is safe to run against a device until every placeholder has been replaced.

## Prerequisites

- Terraform 1.9.0 or newer. The IOS-XE module requires it. 1.8.0 is enough for the IOS-XR module alone.
- Network reachability to the devices.
- IOS-XE: NETCONF on TCP 830. The provider defaults to NETCONF. A host may be written as `ip:port`.
- IOS-XR: gNMI on TCP 57400, with `grpc` enabled on the device. Set `IOSXR_TLS=true` when the device presents TLS. `IOSXR_VERIFY_CERTIFICATE` defaults to false.
- One credential pair per root. Every device in that root uses the same username and password.

## Credentials

Do not put usernames or passwords in the YAML. The published modules read them from the environment.

| Platform | Variables |
| --- | --- |
| IOS-XE | `IOSXE_USERNAME`, `IOSXE_PASSWORD` |
| IOS-XR | `IOSXR_USERNAME`, `IOSXR_PASSWORD` |

`nac-iosxe` 1.0.0 ignores a `provider "iosxe"` username and password block. Environment variables are the supported path for that module. `nac-iosxr` 0.1.1 uses the same environment variables when the provider block does not set them.

`.gitignore` excludes `*.tfvars`, `.terraform/`, and state files. A local `terraform.tfvars` is the place for any root variables you add later. `terraform.tfvars.example` in each root shows the environment variables and is safe to commit because it has no secrets. Never commit a tfvars file, a state file, or a YAML file after the placeholders have been replaced with real keys.

## Why two roots

`netascode/nac-iosxe/iosxe` 1.0.0 requires `netascode/utils` `>= 2.0.2, < 3.0.0`. `netascode/nac-iosxr/iosxr` 0.1.1 requires `netascode/utils` `= 1.1.0-beta5`. Those constraints cannot be met in one Terraform configuration, and provider versions are configuration-wide. Each platform therefore has its own root:

| Root | Module | Provider |
| --- | --- | --- |
| `iosxe/` | `netascode/nac-iosxe/iosxe` 1.0.0 | `CiscoDevNet/iosxe` 1.0.0 |
| `iosxr/` | `netascode/nac-iosxr/iosxr` 0.1.1 | `CiscoDevNet/iosxr` 0.7.1 |

`nac-iosxr` 0.1.1 is a maintained module, so IOS-XR uses it rather than a hand-written `yamldecode()` layer. Provider and module versions above are pinned. They were taken from the module `versions.tf` on tags `v1.0.0` and `v0.1.1`, not from the default branch. The IOS-XE module allows `iosxe >= 1.0.0`; this root pins `1.0.0`, which is the release that tag was tested with. GitHub `main` of `nac-iosxe` is an older schema and is not the source for these files.

## Data model

Each root has `data/defaults.nac.yaml` and `data/devices/<device>.nac.yaml`.

- `defaults.nac.yaml` holds the `enterprise-baseline` device group: banners, domain, NTP, logging, AAA or TACACS, SSH, SNMPv3, LLDP and CDP, the management VRF, and the management ACLs.
- The device file sets `name`, `host`, `device_groups`, hostname, interface addresses, the management default route, and one routing process.

NaC merges every `*.yaml` and `*.yml` file under `data/`. A device that lists `enterprise-baseline` inherits that group's `configuration`. Values on the device replace the same keys from the group. Add another device by copying the device file and changing the name, host, and addresses.

Interface identifiers that are not a plain integer use the NaC `"$string "` prefix, for example `id: "$string 0/0"`. The interface resources strip that prefix before they build the interface name. OSPF `non_passive_interfaces.interface_id` in `nac-iosxe` 1.0.0 is copied as the interface name with no prefix strip, so that field is the raw id (`0/0`).

### IOS-XE example (`edge-xe-01`)

The group plus `data/devices/edge-xe-01.nac.yaml` covers:

- hostname, domain, and UTC clock
- local user `LOCAL-ADMIN` (secret type 0 placeholder) and enable secret
- TACACS+ group `TACACS-SERVERS` in `Mgmt-vrf`, with local fallback on login
- AAA authorization and accounting
- SSHv2, VTY ACL, console login list `CONSOLE`, AUX transport output none
- banners, NTP HMAC-SHA-256 in `Mgmt-vrf`, buffered logging and syslog
- SNMPv3 authPriv (`sha-2-256` / AES) restricted by `ACL-SNMP`
- LLDP and CDP globally enabled; CDP disabled on the example edge interface
- `Mgmt-vrf` on `GigabitEthernet0`, plus `GigabitEthernet0/0`
- OSPF process 1, passive by default, area 0 on the example interface

`nac-iosxe` 1.0.0 does not model per-interface LLDP, SSH algorithm lists, `login block-for`, or `ntp allow mode control`. Those remain in the CLI template only.

### IOS-XR example (`core-xr-01`)

The group plus `data/devices/core-xr-01.nac.yaml` covers:

- hostname and domain lookup disabled
- banners, service timestamps, and console and monitor logging disabled
- NTP HMAC-SHA2 in `Mgmt-vrf`, with `update-calendar`
- syslog and SNMPv3 authPriv (HMAC-SHA `sha`, AES-256). Classic SNMPv3 on 7.5 and 24.x accepts `sha`. `sha-256` is the `secure-v3` CLI from 26.3.1
- SSHv2, HMAC-SHA1 disabled, and Telnet `max-servers 0` in the default VRF and `Mgmt-vrf`
- VTY access-class and SSH access-list `ACL-VTY-MGMT`
- LLDP on, CDP explicitly off, LLDP transmit and receive disabled on the example interface
- `Mgmt-vrf` on `MgmtEth0/RP0/CPU0/0`, plus `GigabitEthernet0/0/0/1`
- IS-IS process `CORE`, level-2-only, wide metrics, point-to-point on the example interface

`nac-iosxr` 0.1.1 has no username or AAA method-list resources (the module still has a TODO for AAA). The device file supplies those as `cli_templates`. Telnet is supplied the same way. `CiscoDevNet/iosxr` 0.7.1 rejects `ipv4_server_max_servers` and `ipv6_server_max_servers` outside 1–100, so the `telnet` YAML resource cannot set `max-servers 0`.

Each template is one command. The module joins every line of a template with spaces before it calls `iosxr_cli`, and provider 0.7.1 places that string inside a JSON quote without escaping it, so a raw newline is not a valid gNMI value. `aaa password-policy` takes one keyword per invocation (`min-length`, `max-length`, `upper-case`, `lower-case`, `numeric`, `special-char`). `username` takes one clause per invocation (`group`, `password-policy`, or `secret`). The secret template is a later order so the policy is attached first. The local user is `LOCAL-ADMIN` with secret type 0 placeholder `<LOCAL_ADMIN_SECRET>`.

Remote syslog severity uses the host enum `info`. Buffered logging and `trap` use a different enum, `informational`. `logging monitor disable` is the provider choice `disable`.

TACACS hosts use the global `tacacs-server host` resource. The key leaves accept type 6 or type 7 material, not cleartext, so `<TACACS_KEY>` has to be replaced with the encrypted form before apply. VRF `server-private` groups from the CLI template are not in this module version. Login methods use `group tacacs+`, which matches those global hosts.

SNMPv3 passwords on IOS-XR use the default-encryption leaf, which allows only `[0-9a-zA-Z]`. The placeholders are `SNMPV3AUTHSECRET` and `SNMPV3PRIVSECRET`. The NTP HMAC-SHA2 value is stored in the encrypted key leaf.

## Check the configuration

From each root, after `terraform init`:

```bash
terraform fmt -check
terraform validate
```

`validate` checks the Terraform configuration and the provider schema. It does not log in to a device and it does not prove that a placeholder will be accepted as a key.
