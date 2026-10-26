# IOS-XR

Configuration templates for Cisco IOS-XR.

## Base template

[`IOS-XR-base-config.cfg`](IOS-XR-base-config.cfg) is a hardened management baseline for current IOS-XR 7.5 and later, including 24.x (ASR 9000, NCS 540/5500/5700, Cisco 8000). It uses the IOS-XR commit model and IOS-XR command syntax. It is not an IOS-XE configuration with different prompts.

Differences from the IOS-XE baseline that matter when you paste:

- Changes are staged. Apply with `configure exclusive`, review `show configuration`, then `commit confirmed 120`. Confirm reachability and issue `commit` before the timer expires.
- There is no privilege 15 and no enable secret. The local admin is a `root-lr` user. `secret 0` is rewritten to a type 10 SHA-512 hash on commit.
- The management interface uses `vrf Mgmt-vrf`, not `vrf forwarding`.
- AAA command authorization is `aaa authorization commands` (no privilege level). The fallback method is `none`, which is used only when the TACACS+ group is unreachable. A TACACS deny still denies the command.
- SSH is bound to the management VRF with `ssh server vrf`. Telnet is shut off with `telnet vrf ... server max-servers 0`. VTY settings go on `line default`, not `line vty`.
- Logging, NTP, and static routes are hierarchical. NTP authentication uses the `sha2` key type (HMAC-SHA2, added in 7.5.1).
- SNMP traps are `snmp-server traps ...`, not `snmp-server enable traps`.

The template sets hostname and domain, a management VRF and static default, TACACS+ with local fallback, SSHv2 only, a VTY ACL, banners, authenticated NTP, buffered logging plus a syslog host, SNMPv3 authPriv, an LLDP-on / CDP-off stance, `no ipv4 source-route`, and an example untrusted edge interface.

CDP is left unconfigured (disabled). LLDP is enabled globally and turned off on the example edge. Enable CDP only on links that actually need Cisco neighbor discovery.

AES privacy for SNMPv3 requires the k9sec security package. HMAC-SHA2 NTP keys are not compatible with stock ntpd or chrony, which do not speak Cisco's HMAC variant. A commented MD5 key line is in the template for those servers.

Do not commit a filled-in copy of this file.

## Placeholders

Replace every token below. Secrets must not contain spaces, question marks, or angle brackets.

| Placeholder | Meaning |
| --- | --- |
| `<HOSTNAME>` | Device hostname |
| `<DOMAIN_NAME>` | Domain name |
| `<TIMEZONE>` | Timezone label, for example `UTC` or `PST` |
| `<TZ_OFFSET>` | Hours from UTC, for example `0` or `-8` |
| `<LOCAL_ADMIN_USER>` | Break-glass local username (`root-lr`) |
| `<LOCAL_ADMIN_SECRET>` | Break-glass password; commit rewrites it to secret type 10. Must satisfy the password policy (15+ characters, upper, lower, digit, special) |
| `<MGMT_INTERFACE>` | Management interface id as the CLI accepts it, for example `MgmtEth0/RP0/CPU0/0` (NCS, 8000) or `MgmtEth0/RSP0/CPU0/0` (ASR 9000) |
| `<MGMT_IP>` | Management IPv4 address |
| `<MGMT_PREFIX>` | Prefix length only, for example `24` |
| `<MGMT_GATEWAY>` | Default gateway inside `Mgmt-vrf` |
| `<TACACS_SERVER>` | Primary TACACS+ server IPv4 address |
| `<TACACS_SERVER_SECONDARY>` | Secondary TACACS+ server IPv4 address |
| `<TACACS_KEY>` | TACACS+ shared key (replace on each server if the keys differ) |
| `<MGMT_STATION_NET>` | IPv4 network allowed to SSH |
| `<MGMT_STATION_PREFIX>` | Prefix length of that network |
| `<NTP_KEY_ID>` | NTP key number |
| `<NTP_KEY>` | NTP HMAC-SHA2 key |
| `<NTP_SERVER>` | Primary NTP server IPv4 address |
| `<NTP_SERVER_SECONDARY>` | Secondary NTP server IPv4 address |
| `<SYSLOG_SERVER>` | Syslog collector IPv4 address |
| `<SNMP_CONTACT>` | SNMPv3 contact string |
| `<SNMP_LOCATION>` | SNMPv3 location string |
| `<SNMPV3_GROUP>` | SNMPv3 group name |
| `<SNMPV3_USER>` | SNMPv3 username |
| `<SNMPV3_AUTH_SECRET>` | SNMPv3 authentication secret (HMAC-SHA) |
| `<SNMPV3_PRIV_SECRET>` | SNMPv3 privacy secret (AES-256); must differ from the auth secret |
| `<NMS_NET>` | NMS network allowed to poll SNMP |
| `<NMS_PREFIX>` | Prefix length of the NMS network |
| `<SNMP_TRAP_HOST>` | SNMP trap receiver IPv4 address |
| `<EXAMPLE_INTERFACE>` | Example edge interface, for example `HundredGigE0/0/0/0` |
| `<IF_DESCRIPTION>` | Description for that interface |
| `<IF_IP>` | IPv4 address for that interface |
| `<IF_PREFIX>` | Prefix length for that interface |

Optional, left commented in the template: `<DNS_SERVER>`.

The VRF name `Mgmt-vrf` is literal. Change every occurrence if the platform already uses a different management VRF.
