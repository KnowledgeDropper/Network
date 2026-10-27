# Cisco ISE Network-as-Code template library

Complete, schema-validated YAML templates for the NaC **ISE** data model - every model page under <https://netascode.cisco.com/docs/data_models/ise/> and every attribute of the published JSON Schema (<https://github.com/netascode/schema>, `schema.json`, top-level key `ise:`).

> These are **templates**, not a deployable design: every optional attribute is set so you can see it. Copy the blocks you need into your own `data/` and delete the rest before `terraform plan` against a real system.

## Versions (verified on registry.terraform.io, 2026-10-27)

| Component | Version |
|---|---|
| Module `netascode/nac-ise/ise` | `1.1.0` (latest) |
| Provider `CiscoDevNet/ise` | `0.5.2` (latest) |
| Terraform | `>= 1.11.0` (tested with 1.17.0) |
| Other providers | netascode/utils `2.0.0` (pinned by the module), hashicorp/local `>= 2.3.0`, hashicorp/time `>= 0.10.0` |

## Usage

```bash
export ISE_URL=... ISE_USERNAME=... ISE_PASSWORD=...   # credentials only via env vars
# plus every secret referenced with `!env` in data/*.nac.yaml (list below)
terraform init && terraform validate
python3 -m venv .venv && .venv/bin/pip install jsonschema pyyaml
.venv/bin/python scripts/validate_schema.py --full .     # schema + light reference checks, also with #~ alternatives enabled
terraform plan
```

Provider credentials: ISE_URL, ISE_USERNAME, ISE_PASSWORD; optional ISE_INSECURE, ISE_RETRIES, ISE_REQUEST_TIMEOUT. Nothing is hard-coded in `main.tf`.

## Conventions used in every file

- Inline comment per attribute: `MANDATORY` / `optional` (from the doc tables; `conditional/variant-mandatory` when the docs show two variants that disagree), `choices:` (enum), `range:`, `regex:`, `maxlen:`, `default:` (doc/schema defaults).
- `optional (schema-only, not on docs page)` = present in netascode/schema but not (yet) on the docs site.
- `WARN: not referenced by nac-ise 1.1.0 module code` = accepted by the schema (main branch) but not consumed by the pinned module release - it will be silently ignored.
- Lines prefixed `#~` are **mutually exclusive alternatives** (e.g. `certificate` vs `certificate_file`, static vs DHCP/PPPoE addressing, PSK vs certificate auth). They are kept schema-valid; the validator checks them with `--full`.
- Secrets are never inline: `!env VAR` tags are resolved by `netascode/utils` `yaml_merge` at plan time.
- Names are consistent across files so references resolve (e.g. access rules reference zones/objects defined in the object files).
- Addressing uses RFC 1918 / RFC 5737 (192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24) / RFC 3849 (2001:db8::/32); names use example.com.
- Recursive structures (`children` of groups and conditions) are shown 2-3 levels deep; the schema allows deeper nesting with the same structure.

## Files

| File | Content | Doc pages covered |
|---|---|---|
| `data/system.nac.yaml` | ISE system: backup/patch repositories and licensing tiers. | License, Repository |
| `data/network_resources.nac.yaml` | ISE Network Resources: Network Device Groups and Network Devices (RADIUS/TACACS+/SNMP/TrustSec). | Network Device, Network Device Group |
| `data/identity_management.nac.yaml` | ISE Identity Management: user identity groups, internal users, AD join points, certificate auth profiles, identity source sequences. | Active Directory, Certificate Authentication Profile, Identity Source Sequence, Internal User, User Identity Group |
| `data/endpoints.nac.yaml` | ISE endpoints: endpoint identity groups, endpoint custom attributes, static endpoints. | Endpoint, Endpoint Custom Attribute, Endpoint Identity Group |
| `data/trust_sec.nac.yaml` | ISE TrustSec: SGTs, SGACLs, IP-SGT static mappings (+groups), egress matrix/matrices, work-process settings. | IP SGT Mapping, IP SGT Mapping Group, Matrices, Matrix Entry, Security Group, Security Group ACL |
| `data/network_access_policy_elements.nac.yaml` | ISE Network Access policy elements: library conditions, time/date conditions, allowed protocols, dACLs, authorization profiles, dictionaries. | Allowed Protocols, Authorization Profile, Condition, Dictionary, Dictionary Attribute, Downloadable ACL, Time Date Condition |
| `data/network_access_policy_sets.nac.yaml` | ISE Network Access policy sets: authentication, authorization, local + global exception rules. | Authentication Rule, Authorization Exception Rule, Authorization Global Exception Rule, Authorization Rule, Policy Set |
| `data/device_admin_policy_elements.nac.yaml` | ISE Device Administration (TACACS+) policy elements: conditions, time/date, allowed protocols, TACACS profiles + command sets. | Allowed Protocols, Condition, TACACS Command Set, TACACS Profile, Time Date Condition |
| `data/device_admin_policy_sets.nac.yaml` | ISE Device Administration policy sets: authentication, authorization, local + global exception rules. | Authentication Rule, Authorization Exception Rule, Authorization Global Exception Rule, Authorization Rule, Policy Set |

## Coverage: docs model pages -> template file

40 model pages found (crawled from the site sitemap, since the section index URLs return 404) + 2 non-model pages (overview/features).

| # | Doc page | Model path(s) | File | Status |
|---|---|---|---|---|
| 1 | [Allowed Protocols](https://netascode.cisco.com/docs/data_models/ise/device_admin/device_admin_allowed_protocols/) | `ise.device_administration.policy_elements.allowed_protocols` | device_admin_policy_elements.nac.yaml | covered (5 attribute lines) |
| 2 | [Authentication Rule](https://netascode.cisco.com/docs/data_models/ise/device_admin/device_admin_authentication_rule/) | `ise.device_administration.policy_sets.authentication_rules` | device_admin_policy_sets.nac.yaml | covered (16 attribute lines) |
| 3 | [Authorization Exception Rule](https://netascode.cisco.com/docs/data_models/ise/device_admin/device_admin_authorization_exception_rule/) | `ise.device_administration.policy_sets.authorization_exception_rules` | device_admin_policy_sets.nac.yaml | covered (14 attribute lines) |
| 4 | [Authorization Global Exception Rule](https://netascode.cisco.com/docs/data_models/ise/device_admin/device_admin_authorization_global_exception_rule/) | `ise.device_administration.authorization_global_exception_rules` | device_admin_policy_sets.nac.yaml | covered (14 attribute lines) |
| 5 | [Authorization Rule](https://netascode.cisco.com/docs/data_models/ise/device_admin/device_admin_authorization_rule/) | `ise.device_administration.policy_sets.authorization_rules` | device_admin_policy_sets.nac.yaml | covered (20 attribute lines) |
| 6 | [Condition](https://netascode.cisco.com/docs/data_models/ise/device_admin/device_admin_condition/) | `ise.device_administration.policy_elements.conditions` | device_admin_policy_elements.nac.yaml | covered (21 attribute lines) |
| 7 | [Policy Set](https://netascode.cisco.com/docs/data_models/ise/device_admin/device_admin_policy_set/) | `ise.device_administration.policy_sets` | device_admin_policy_sets.nac.yaml | covered (71 attribute lines) |
| 8 | [TACACS Command Set](https://netascode.cisco.com/docs/data_models/ise/device_admin/device_admin_tacacs_command_set/) | `ise.device_administration.policy_elements.tacacs_command_sets` | device_admin_policy_elements.nac.yaml | covered (6 attribute lines) |
| 9 | [TACACS Profile](https://netascode.cisco.com/docs/data_models/ise/device_admin/device_admin_tacacs_profile/) | `ise.device_administration.policy_elements.tacacs_profiles` | device_admin_policy_elements.nac.yaml | covered (5 attribute lines) |
| 10 | [Time Date Condition](https://netascode.cisco.com/docs/data_models/ise/device_admin/device_admin_time_date_condition/) | `ise.device_administration.policy_elements.time_date_conditions` | device_admin_policy_elements.nac.yaml | covered (13 attribute lines) |
| 11 | [Features](https://netascode.cisco.com/docs/data_models/ise/features/) | - | - | n/a (non-model page) |
| 12 | [Active Directory](https://netascode.cisco.com/docs/data_models/ise/identity_management/active_directory/) | `ise.identity_management.active_directories` | identity_management.nac.yaml | covered (43 attribute lines) |
| 13 | [Certificate Authentication Profile](https://netascode.cisco.com/docs/data_models/ise/identity_management/certificate_authentication_profile/) | `ise.identity_management.certificate_authentication_profiles` | identity_management.nac.yaml | covered (7 attribute lines) |
| 14 | [Endpoint](https://netascode.cisco.com/docs/data_models/ise/identity_management/endpoint/) | `ise.identity_management.endpoints` | endpoints.nac.yaml | covered (25 attribute lines) |
| 15 | [Endpoint Custom Attribute](https://netascode.cisco.com/docs/data_models/ise/identity_management/endpoint_custom_attribute/) | `ise.identity_management.endpoint_custom_attributes` | endpoints.nac.yaml | covered (2 attribute lines) |
| 16 | [Endpoint Identity Group](https://netascode.cisco.com/docs/data_models/ise/identity_management/endpoint_identity_group/) | `ise.identity_management.endpoint_identity_groups` | endpoints.nac.yaml | covered (7 attribute lines) |
| 17 | [Identity Source Sequence](https://netascode.cisco.com/docs/data_models/ise/identity_management/identity_source_sequence/) | `ise.identity_management.identity_source_sequences` | identity_management.nac.yaml | covered (5 attribute lines) |
| 18 | [Internal User](https://netascode.cisco.com/docs/data_models/ise/identity_management/internal_user/) | `ise.identity_management.internal_users` | identity_management.nac.yaml | covered (16 attribute lines) |
| 19 | [User Identity Group](https://netascode.cisco.com/docs/data_models/ise/identity_management/user_identity_group/) | `ise.identity_management.user_identity_groups` | identity_management.nac.yaml | covered (7 attribute lines) |
| 20 | [Allowed Protocols](https://netascode.cisco.com/docs/data_models/ise/network_access/network_access_allowed_protocols/) | `ise.network_access.policy_elements.allowed_protocols` | network_access_policy_elements.nac.yaml | covered (75 attribute lines) |
| 21 | [Authentication Rule](https://netascode.cisco.com/docs/data_models/ise/network_access/network_access_authentication_rule/) | `ise.network_access.policy_sets.authentication_rules` | network_access_policy_sets.nac.yaml | covered (16 attribute lines) |
| 22 | [Authorization Exception Rule](https://netascode.cisco.com/docs/data_models/ise/network_access/network_access_authorization_exception_rule/) | `ise.network_access.policy_sets.authorization_exception_rules` | network_access_policy_sets.nac.yaml | covered (14 attribute lines) |
| 23 | [Authorization Global Exception Rule](https://netascode.cisco.com/docs/data_models/ise/network_access/network_access_authorization_global_exception_rule/) | `ise.network_access.authorization_global_exception_rules` | network_access_policy_sets.nac.yaml | covered (14 attribute lines) |
| 24 | [Authorization Profile](https://netascode.cisco.com/docs/data_models/ise/network_access/network_access_authorization_profile/) | `ise.network_access.policy_elements.authorization_profiles` | network_access_policy_elements.nac.yaml | covered (35 attribute lines) |
| 25 | [Authorization Rule](https://netascode.cisco.com/docs/data_models/ise/network_access/network_access_authorization_rule/) | `ise.network_access.policy_sets.authorization_rules` | network_access_policy_sets.nac.yaml | covered (20 attribute lines) |
| 26 | [Condition](https://netascode.cisco.com/docs/data_models/ise/network_access/network_access_condition/) | `ise.network_access.policy_elements.conditions` | network_access_policy_elements.nac.yaml | covered (22 attribute lines) |
| 27 | [Dictionary](https://netascode.cisco.com/docs/data_models/ise/network_access/network_access_dictionary/) | `ise.network_access.policy_elements.dictionaries` | network_access_policy_elements.nac.yaml | covered (9 attribute lines) |
| 28 | [Dictionary Attribute](https://netascode.cisco.com/docs/data_models/ise/network_access/network_access_dictionary_attribute/) | `ise.network_access.policy_elements.dictionaries.attributes` | network_access_policy_elements.nac.yaml | covered (5 attribute lines) |
| 29 | [Downloadable ACL](https://netascode.cisco.com/docs/data_models/ise/network_access/network_access_downloadable_acl/) | `ise.network_access.policy_elements.downloadable_acls` | network_access_policy_elements.nac.yaml | covered (4 attribute lines) |
| 30 | [Policy Set](https://netascode.cisco.com/docs/data_models/ise/network_access/network_access_policy_set/) | `ise.network_access.policy_sets` | network_access_policy_sets.nac.yaml | covered (71 attribute lines) |
| 31 | [Time Date Condition](https://netascode.cisco.com/docs/data_models/ise/network_access/network_access_time_date_condition/) | `ise.network_access.policy_elements.time_date_conditions` | network_access_policy_elements.nac.yaml | covered (13 attribute lines) |
| 32 | [Network Device](https://netascode.cisco.com/docs/data_models/ise/network_resources/network_device/) | `ise.network_resources.network_devices` | network_resources.nac.yaml | covered (60 attribute lines) |
| 33 | [Network Device Group](https://netascode.cisco.com/docs/data_models/ise/network_resources/network_device_group/) | `ise.network_resources.network_device_groups` | network_resources.nac.yaml | covered (7 attribute lines) |
| 34 | [Overview](https://netascode.cisco.com/docs/data_models/ise/overview/) | - | - | n/a (non-model page) |
| 35 | [License](https://netascode.cisco.com/docs/data_models/ise/system/license/) | `ise.system.licenses` | system.nac.yaml | covered (2 attribute lines) |
| 36 | [Repository](https://netascode.cisco.com/docs/data_models/ise/system/repository/) | `ise.system.repositories` | system.nac.yaml | covered (8 attribute lines) |
| 37 | [IP SGT Mapping](https://netascode.cisco.com/docs/data_models/ise/trust_sec/ip_sgt_mapping/) | `ise.trust_sec.ip_sgt_mappings` | trust_sec.nac.yaml | covered (7 attribute lines) |
| 38 | [IP SGT Mapping Group](https://netascode.cisco.com/docs/data_models/ise/trust_sec/ip_sgt_mapping_group/) | `ise.trust_sec.ip_sgt_mapping_groups` | trust_sec.nac.yaml | covered (4 attribute lines) |
| 39 | [Matrices](https://netascode.cisco.com/docs/data_models/ise/trust_sec/matrices/) | `ise.trust_sec.matrices` | trust_sec.nac.yaml | covered (8 attribute lines) |
| 40 | [Matrix Entry](https://netascode.cisco.com/docs/data_models/ise/trust_sec/matrix_entry/) | `ise.trust_sec.matrix_entries` | trust_sec.nac.yaml | covered (4 attribute lines) |
| 41 | [Security Group](https://netascode.cisco.com/docs/data_models/ise/trust_sec/security_group/) | `ise.trust_sec.security_groups` | trust_sec.nac.yaml | covered (4 attribute lines) |
| 42 | [Security Group ACL](https://netascode.cisco.com/docs/data_models/ise/trust_sec/security_group_acl/) | `ise.trust_sec.security_group_acls` | trust_sec.nac.yaml | covered (4 attribute lines) |

Schema attribute coverage: 527/527 distinct attribute paths of `ise:` (recursive `children` collapsed) are present in the templates; 0 missing.

## Environment variables referenced by `!env` tags

| Variable | Used at |
|---|---|
| `ISE_IDENTITY_MANAGEMENT_ACTIVE_DIRECTORIES_AD_PASSWORD` | `ise.identity_management.active_directories.ad_password` |
| `ISE_IDENTITY_MANAGEMENT_INTERNAL_USERS_ENABLE_PASSWORD` | `ise.identity_management.internal_users.enable_password` |
| `ISE_IDENTITY_MANAGEMENT_INTERNAL_USERS_PASSWORD` | `ise.identity_management.internal_users.password` |
| `ISE_NETWORK_DEVICES_RADIUS_ENCRYPTION_KEY` | `ise.network_resources.network_devices.radius.encryption_key` |
| `ISE_NETWORK_DEVICES_RADIUS_MESSAGE_AUTHENTICATOR_CODE_KEY` | `ise.network_resources.network_devices.radius.message_authenticator_code_key` |
| `ISE_NETWORK_DEVICES_RADIUS_SECOND_SHARED_SECRET` | `ise.network_resources.network_devices.radius.second_shared_secret` |
| `ISE_NETWORK_DEVICES_RADIUS_SHARED_SECRET` | `ise.network_resources.network_devices.radius.shared_secret` |
| `ISE_NETWORK_DEVICES_SNMP_AUTH_PASSWORD` | `ise.network_resources.network_devices.snmp.auth_password` |
| `ISE_NETWORK_DEVICES_SNMP_PRIVACY_PASSWORD` | `ise.network_resources.network_devices.snmp.privacy_password` |
| `ISE_NETWORK_DEVICES_SNMP_RO_COMMUNITY` | `ise.network_resources.network_devices.snmp.ro_community` |
| `ISE_NETWORK_DEVICES_TACACS_SHARED_SECRET` | `ise.network_resources.network_devices.tacacs.shared_secret` |
| `ISE_NETWORK_DEVICES_TRUST_SEC_DEVICE_PASSWORD` | `ise.network_resources.network_devices.trust_sec.device_password` |
| `ISE_NETWORK_DEVICES_TRUST_SEC_ENABLE_MODE_PASSWORD` | `ise.network_resources.network_devices.trust_sec.enable_mode_password` |
| `ISE_NETWORK_DEVICES_TRUST_SEC_EXEC_MODE_PASSWORD` | `ise.network_resources.network_devices.trust_sec.exec_mode_password` |
| `ISE_NETWORK_DEVICES_TRUST_SEC_REST_API_PASSWORD` | `ise.network_resources.network_devices.trust_sec.rest_api_password` |
| `ISE_SYSTEM_REPOSITORIES_PASSWORD` | `ise.system.repositories.password` |

## Validation performed (2026-10-27)

| Check | Result |
|---|---|
| Merged `data/*.nac.yaml` vs netascode/schema `schema.json` (Draft 2020-12, `additionalProperties: false`) | 0 errors |
| Same, with every `#~` alternative uncommented (`--full`) | 0 errors |
| Real `provider::utils::yaml_merge` (netascode/utils 2.0.0, `!env` resolved) output vs schema | 0 errors; identical to the Python merge used by the validator |
| Light reference checks (allowed protocols, authz profiles, TACACS profiles/command sets, SGTs, SGACLs, user groups, dACLs) | 0 errors |
| `terraform fmt -check`, `terraform init`, `terraform validate` | success |
| `terraform plan/apply` | **not run** - would require contacting ISE (out of scope) |

## Gaps, caveats and assumptions

- **Not modelled by NaC ISE** (no docs page and no schema key): guest/sponsor portals and guest types, posture, profiler policies, client provisioning, certificates/system certificates, deployment/node settings, pxGrid, SMTP/syslog remote logging. "System" in the data model is only repositories + licenses.
- **Docs vs schema:** the Endpoint page shows `profile_id`, which the schema rejects - omitted (use `profile_name`).
- `teap.request_basic_pwd_auth` is in the schema but not referenced by nac-ise 1.1.0 module code (marked `WARN`).
- Conditions: every condition shows all node types - `ConditionAttributes`, `ConditionReference` (to library conditions defined in the policy-elements files), `ConditionAndBlock`/`ConditionOrBlock`, `is_negate` and `dictionary_value` (attribute-to-attribute compare). Library conditions use the `Library*` types. Nesting is shown 2 levels deep; ISE/schema allow more.
- Built-in names are used where ISE ships them (`Internal Users`, `Internal Endpoints`, `Profiled`, `Self-Registered Guest Portal (default)`, NDG roots `Location#All Locations`, `Device Type#All Device Types`, `IPSEC#Is IPSEC Device#No`). `CORP_AD` dictionary/attribute values in conditions assume the AD join point defined in `identity_management.nac.yaml`.
- Templates intentionally enable more than a real policy would (e.g. both wired and wireless ACL attributes in one authorization profile). They are schema-valid, not a design.
- Values for attributes the docs don't exemplify are realistic placeholders chosen by type/name; review enums against your ISE version (provider tested with ISE 3.3-3.5).
