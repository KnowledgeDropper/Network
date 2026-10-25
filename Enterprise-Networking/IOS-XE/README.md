# IOS-XE

Configuration templates for Cisco IOS-XE.

## Base template

[`IOS-XE-base-config.cfg`](IOS-XE-base-config.cfg) is a hardened management baseline for current IOS-XE 17.12 and later (Catalyst 9000, Catalyst 8000, ISR, ASR). It is a starting configuration, not a campus design. It does not configure routing protocols, QoS, or SD-Access.

The template sets:

- Hostname, domain name, and timezone
- A management VRF (`Mgmt-vrf`) with a default route
- Local break-glass admin (scrypt / type 9) and an enable secret (scrypt)
- TACACS+ authentication with local fallback, console kept on the local user
- SSHv2 only, a pinned modern algorithm set, VTY ACL, and HTTP/HTTPS disabled
- Login banners, login failure lockout, and an auxiliary port with no exec
- Authenticated NTP, buffered logging plus a syslog host, and timestamps
- SNMPv3 authPriv only, with USM and VACM excluded from the read view
- LLDP and CDP enabled globally, and disabled on the example untrusted edge
- Service hardening (no source routing, no BOOTP, TCP keepalives, AES type-6 key encryption)
- An example untrusted Layer 3 edge interface

Switch-only commands (VTP, Rapid-PVST, BPDU Guard, errdisable recovery, UDLD) are commented so the file still pastes on a router. Uncomment that section on Catalyst LAN switches.

Apply it from a console session. Keep that session open, then test a new SSH session before you disconnect. Generate the SSH host key after the domain name is configured:

```text
crypto key generate rsa modulus 4096
```

`password encryption aes` stores TACACS, NTP, and similar keys as type 6. The master key is not displayed in `show running-config`. Type 9 user secrets do not depend on that master key. Do not commit a filled-in copy of this file.

On Catalyst 9000, `GigabitEthernet0/0` is already in `Mgmt-vrf`. On ISR, ASR, and Catalyst 8000, point `<MGMT_INTERFACE>` at the real management port (often `GigabitEthernet0`).

## Placeholders

Replace every token below. Secrets must not contain spaces, question marks, or angle brackets.

| Placeholder | Meaning |
| --- | --- |
| `<HOSTNAME>` | Device hostname |
| `<DOMAIN_NAME>` | DNS domain used in the SSH key name |
| `<TIMEZONE>` | Timezone label, for example `UTC` or `EST` |
| `<TZ_OFFSET>` | Hours from UTC, for example `0` or `-5` |
| `<CONFIG_ENCRYPT_KEY>` | Master key for type-6 reversible encryption (16+ characters) |
| `<LOCAL_ADMIN_USER>` | Break-glass local username |
| `<LOCAL_ADMIN_SECRET>` | Break-glass password; the device stores it as a type 9 scrypt hash |
| `<ENABLE_SECRET>` | Enable secret; stored as type 9 scrypt |
| `<MGMT_INTERFACE>` | Management interface, for example `GigabitEthernet0/0` |
| `<MGMT_IP>` | Management IPv4 address |
| `<MGMT_MASK>` | Management dotted mask, for example `255.255.255.0` |
| `<MGMT_GATEWAY>` | Default gateway inside `Mgmt-vrf` |
| `<TACACS_SERVER>` | Primary TACACS+ server IPv4 address |
| `<TACACS_SERVER_SECONDARY>` | Secondary TACACS+ server IPv4 address |
| `<TACACS_KEY>` | TACACS+ shared key (replace on each server line if the keys differ) |
| `<MGMT_STATION_NET>` | Network allowed to SSH, standard-ACL address |
| `<MGMT_STATION_WILDCARD>` | Wildcard mask for that network |
| `<BREAKGLASS_NET>` | Hosts exempt from login quiet-mode |
| `<BREAKGLASS_WILDCARD>` | Wildcard mask for the quiet-mode exemption |
| `<NTP_KEY_ID>` | NTP key number, 1-4294967295 |
| `<NTP_KEY>` | NTP HMAC-SHA2-256 key (1-32 bytes) |
| `<NTP_SERVER>` | Primary NTP server IPv4 address |
| `<NTP_SERVER_SECONDARY>` | Secondary NTP server IPv4 address |
| `<SYSLOG_SERVER>` | Syslog collector IPv4 address |
| `<SNMP_CONTACT>` | SNMPv3 contact string |
| `<SNMP_LOCATION>` | SNMPv3 location string |
| `<SNMPV3_GROUP>` | SNMPv3 group name |
| `<SNMPV3_USER>` | SNMPv3 username |
| `<SNMPV3_AUTH_SECRET>` | SNMPv3 authentication secret (SHA-2 256) |
| `<SNMPV3_PRIV_SECRET>` | SNMPv3 privacy secret (AES-256); must differ from the auth secret |
| `<NMS_NET>` | NMS network allowed to poll SNMP |
| `<NMS_WILDCARD>` | Wildcard mask for the NMS network |
| `<SNMP_TRAP_HOST>` | SNMP trap receiver IPv4 address |
| `<EXAMPLE_INTERFACE>` | Example edge interface name |
| `<IF_DESCRIPTION>` | Description for that interface |
| `<IF_IP>` | IPv4 address for that interface |
| `<IF_MASK>` | Dotted mask for that interface |

Optional, left commented in the template: `<DNS_SERVER>`.

The VRF name `Mgmt-vrf` is literal. Change every occurrence if the platform already uses a different management VRF.
