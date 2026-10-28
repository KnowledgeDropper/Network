# Cisco FMC Network-as-Code template library

Complete, schema-validated YAML templates for the NaC **FMC** data model - every model page under <https://netascode.cisco.com/docs/data_models/fmc/> and every attribute of the published JSON Schema (<https://github.com/netascode/schema>, `schema.json`, top-level key `fmc:` (+ `existing:`).

> These are **templates**, not a deployable design: every optional attribute is set so you can see it. Copy the blocks you need into your own `data/` and delete the rest before `terraform plan` against a real system.

## Versions (verified on registry.terraform.io, 2026-10-27)

| Component | Version |
|---|---|
| Module `netascode/nac-fmc/fmc` | `0.1.3` (latest) |
| Provider `CiscoDevNet/fmc` | `2.6.1` (latest) |
| Terraform | `>= 1.8.0` (tested with 1.17.0) |
| Other providers | netascode/utils `>= 2.0.0, < 3.0.0`, hashicorp/local `>= 2.3.0, < 3.0.0` |

## Usage

```bash
export FMC_URL=... FMC_USERNAME=... FMC_PASSWORD=...   # credentials only via env vars
# plus every secret referenced with `!env` in data/*.nac.yaml (list below)
terraform init && terraform validate
python3 -m venv .venv && .venv/bin/pip install jsonschema pyyaml
.venv/bin/python scripts/validate_schema.py --full .     # schema + light reference checks, also with #~ alternatives enabled
terraform plan
```

Provider credentials: FMC_URL, FMC_USERNAME, FMC_PASSWORD (or FMC_TOKEN for cdFMC); optional FMC_INSECURE, FMC_RETRIES, FMC_REQTIMEOUT. Nothing is hard-coded in `main.tf`.

## Conventions used in every file

- Inline comment per attribute: `MANDATORY` / `optional` (from the doc tables; `conditional/variant-mandatory` when the docs show two variants that disagree), `choices:` (enum), `range:`, `regex:`, `maxlen:`, `default:` (doc/schema defaults).
- `optional (schema-only, not on docs page)` = present in netascode/schema but not (yet) on the docs site.
- `WARN: not referenced by nac-fmc 0.1.3 module code` = accepted by the schema (main branch) but not consumed by the pinned module release - it will be silently ignored.
- Lines prefixed `#~` are **mutually exclusive alternatives** (e.g. `certificate` vs `certificate_file`, static vs DHCP/PPPoE addressing, PSK vs certificate auth). They are kept schema-valid; the validator checks them with `--full`.
- Secrets are never inline: `!env VAR` tags are resolved by `netascode/utils` `yaml_merge` at plan time.
- Names are consistent across files so references resolve (e.g. access rules reference zones/objects defined in the object files).
- Addressing uses RFC 1918 / RFC 5737 (192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24) / RFC 3849 (2001:db8::/32); names use example.com.
- Recursive structures (`children` of groups and conditions) are shown 2-3 levels deep; the schema allows deeper nesting with the same structure.

## Files

| File | Content | Doc pages covered |
|---|---|---|
| `data/00_global.nac.yaml` | FMC global settings: FMC instance, domains, NaC module behaviour (nac_configuration). | Domain, NAC Configuration |
| `data/objects_network.nac.yaml` | FMC objects: network / port / URL / VLAN / SGT / zones / identity-ish objects. | Application Filter, Dynamic Object, FQDN, Geolocation, Host, ICMPv4, ICMPv6, Interface Group, Network, Network Group, Port, Port Group, Range, Resource Profile, Security Zone, Security Group Tag (SGT), Time Range, Tunnel Zone, URL, URL Group, VLAN Tag, VLAN Tag Group |
| `data/objects_routing.nac.yaml` | FMC objects used by routing/NAT/VPN: ACLs, prefix lists, AS-path, community lists, policy lists, route maps, BFD, SLA monitors, key chains, DNS. | AS Path, BFD Teamplate, DNS Server Group, Expanded Community List, Extended Access List, Extended Community List, IPv4 Prefix List, IPv6 Prefix List, Policy List, Route Map, Standard Access List, Standard Community List |
| `data/objects_vpn_pki.nac.yaml` | FMC objects for VPN/PKI/AAA: IKE/IPsec, certificates, pools, RADIUS/SSO, Secure Client, group policies, service access. | Certificate Enrollment, Certificate Map, External Certificate, Group Policy, IKEv1 IPSec Proposal, IKEv1 Policy, IKEv2 IPSec Proposal, IKEv2 Policy, Internal Certificate, Internal Certificate Authority, IPv4 Address Pool, IPv6 Address Pool, RADIUS Server Group, Secure Client, Service Access, Single Sign On Server (SSO), Trusted Certificate Authority |
| `data/policies_access_control.nac.yaml` | FMC Access Control Policy (rules, categories, default action, logging). | Access Control Policy |
| `data/policies_prefilter.nac.yaml` | FMC Prefilter Policy (prefilter + tunnel rules). | Prefilter Policy |
| `data/policies_nat.nac.yaml` | FMC FTD NAT Policy (auto NAT + manual NAT rules). | FTD NAT Policy |
| `data/policies_threat.nac.yaml` | FMC Intrusion, Network Analysis and Malware & File policies. NOTE: SSL/Decryption, DNS and Identity policies are NOT modelled by NaC FMC (no doc page / schema key). | Marware and File Policy, Intrusion Policy, Network Analysis Policy |
| `data/policies_health.nac.yaml` | FMC Health Policy. | Health Policy |
| `data/devices.nac.yaml` | FTD devices: registration, policy assignment, VRFs, interfaces, static routes, BGP, OSPF, BFD. | BFD, BGP General Settings, BGP IPv4, Device, Device Ether-channel Interface, Device Physical Interface, Device Sub-Interface, IPv4 Static Route, IPv6 Static Route, Loopback Interface, Virtual Tunnel Interface, VRF |
| `data/devices_ha_cluster.nac.yaml` | FTD High Availability pairs and Clusters. NOTE: a device is either standalone, an HA member or a cluster member - adapt names before use. | Cluster, High Availability |
| `data/devices_chassis.nac.yaml` | Multi-instance chassis (Secure Firewall 3100/4200): chassis interfaces + logical devices. | Chassis, Chassis Etherchannel Interface, Chassis Logical Device, Chassis Physical Interface, Chassis Sub-Interface |
| `data/platform_settings.nac.yaml` | FTD Platform Settings policies. | FTD Platform Settings |
| `data/vpns_site_to_site.nac.yaml` | Site-to-Site VPN topologies. | Site to Site |
| `data/vpns_remote_access.nac.yaml` | Remote Access VPN (Secure Client) configuration. | Remote Access |
| `data/integrations.nac.yaml` | Identity integrations: AD/LDAP and Local realms. | AD/LDAP Realm, Local Realm |
| `data/system.nac.yaml` | FMC system: smart licensing, policy assignment on destroy, deployment options. | Deployment, Policy Assignment, Smart License |
| `data/existing.nac.yaml` | Read-only references to objects that already exist on FMC (built-ins, objects owned elsewhere). Names here must exist on FMC; they can be referenced from fmc: like managed objects. | Existing Configuration |

## Coverage: docs model pages -> template file

88 model pages found (crawled from the site sitemap, since the section index URLs return 404) + 2 non-model pages (overview/features).

| # | Doc page | Model path(s) | File | Status |
|---|---|---|---|---|
| 1 | [BFD](https://netascode.cisco.com/docs/data_models/fmc/devices/bfd/) | `fmc.domains.devices.devices.vrfs.bfds` | devices.nac.yaml | covered (6 attribute lines) |
| 2 | [BGP General Settings](https://netascode.cisco.com/docs/data_models/fmc/devices/bgp_general/) | `fmc.domains.devices.devices.bgp_general_settings` | devices.nac.yaml | covered (23 attribute lines) |
| 3 | [BGP IPv4](https://netascode.cisco.com/docs/data_models/fmc/devices/bgp_ipv4/) | `fmc.domains.devices.devices.vrfs.bgp` | devices.nac.yaml | covered (76 attribute lines) |
| 4 | [Chassis](https://netascode.cisco.com/docs/data_models/fmc/devices/chassis/) | `fmc.domains.devices.chassis` | devices_chassis.nac.yaml | covered (44 attribute lines) |
| 5 | [Chassis Etherchannel Interface](https://netascode.cisco.com/docs/data_models/fmc/devices/chassis_etherchannel_interface/) | `fmc.domains.devices.chassis.etherchannel_interfaces` | devices_chassis.nac.yaml | covered (9 attribute lines) |
| 6 | [Chassis Logical Device](https://netascode.cisco.com/docs/data_models/fmc/devices/chassis_logical_device/) | `fmc.domains.devices.chassis.logical_devices` | devices_chassis.nac.yaml | covered (20 attribute lines) |
| 7 | [Chassis Physical Interface](https://netascode.cisco.com/docs/data_models/fmc/devices/chassis_physical_interface/) | `fmc.domains.devices.chassis.physical_interfaces` | devices_chassis.nac.yaml | covered (7 attribute lines) |
| 8 | [Chassis Sub-Interface](https://netascode.cisco.com/docs/data_models/fmc/devices/chassis_sub_interface/) | `fmc.domains.devices.chassis.sub_interfaces` | devices_chassis.nac.yaml | covered (3 attribute lines) |
| 9 | [Cluster](https://netascode.cisco.com/docs/data_models/fmc/devices/cluster/) | `fmc.domains.devices.clusters` | devices_ha_cluster.nac.yaml | covered (11 attribute lines) |
| 10 | [Device](https://netascode.cisco.com/docs/data_models/fmc/devices/device/) | `fmc.domains.devices.devices` | devices.nac.yaml | covered (451 attribute lines) |
| 11 | [Device Ether-channel Interface](https://netascode.cisco.com/docs/data_models/fmc/devices/device_etherchannel_interface/) | `fmc.domains.devices.devices.vrfs.etherchannel_interfaces` | devices.nac.yaml | covered (72 attribute lines) |
| 12 | [Device Physical Interface](https://netascode.cisco.com/docs/data_models/fmc/devices/device_physical_interface/) | `fmc.domains.devices.devices.vrfs.physical_interfaces` | devices.nac.yaml | covered (71 attribute lines) |
| 13 | [Device Sub-Interface](https://netascode.cisco.com/docs/data_models/fmc/devices/device_sub_interface/) | `fmc.domains.devices.devices.vrfs.sub_interfaces` | devices.nac.yaml | covered (61 attribute lines) |
| 14 | [FTD Platform Settings](https://netascode.cisco.com/docs/data_models/fmc/devices/ftd_platform_settings/) | `fmc.domains.devices.ftd_platform_settings` | platform_settings.nac.yaml | covered (111 attribute lines) |
| 15 | [High Availability](https://netascode.cisco.com/docs/data_models/fmc/devices/high_availability/) | `fmc.domains.devices.ha_pairs` | devices_ha_cluster.nac.yaml | covered (29 attribute lines) |
| 16 | [IPv4 Static Route](https://netascode.cisco.com/docs/data_models/fmc/devices/ipv4_static_route/) | `fmc.domains.devices.devices.vrfs.ipv4_static_routes` | devices.nac.yaml | covered (7 attribute lines) |
| 17 | [IPv6 Static Route](https://netascode.cisco.com/docs/data_models/fmc/devices/ipv6_static_route/) | `fmc.domains.devices.devices.vrfs.ipv6_static_routes` | devices.nac.yaml | covered (7 attribute lines) |
| 18 | [Loopback Interface](https://netascode.cisco.com/docs/data_models/fmc/devices/loopback_interface/) | `fmc.domains.devices.devices.vrfs.loopback_interfaces` | devices.nac.yaml | covered (8 attribute lines) |
| 19 | [Virtual Tunnel Interface](https://netascode.cisco.com/docs/data_models/fmc/devices/virtual_tunnel_interface/) | `fmc.domains.devices.devices.vrfs.virtual_tunnel_interfaces` | devices.nac.yaml | covered (17 attribute lines) |
| 20 | [VRF](https://netascode.cisco.com/docs/data_models/fmc/devices/vrf/) | `fmc.domains.devices.devices.vrfs` | devices.nac.yaml | covered (412 attribute lines) |
| 21 | [Domain](https://netascode.cisco.com/docs/data_models/fmc/domains/domains/) | `fmc.domains` | all files (`domains: - name: Global`) | covered (1557 attribute lines) |
| 22 | [Existing Configuration](https://netascode.cisco.com/docs/data_models/fmc/existing/existing/) | `existing.fmc` | existing.nac.yaml | covered (100 attribute lines) |
| 23 | [Features](https://netascode.cisco.com/docs/data_models/fmc/features/) | - | - | n/a (non-model page) |
| 24 | [AD/LDAP Realm](https://netascode.cisco.com/docs/data_models/fmc/integrations/ad_ldap_realm/) | `fmc.domains.integrations.ad_ldap_realms` | integrations.nac.yaml | covered (29 attribute lines) |
| 25 | [Local Realm](https://netascode.cisco.com/docs/data_models/fmc/integrations/local_realm/) | `fmc.domains.integrations.local_realms` | integrations.nac.yaml | covered (2 attribute lines) |
| 26 | [NAC Configuration](https://netascode.cisco.com/docs/data_models/fmc/nac_configuration/nac_configuration/) | `fmc.nac_configuration` | 00_global.nac.yaml | covered (43 attribute lines) |
| 27 | [Application Filter](https://netascode.cisco.com/docs/data_models/fmc/objects/application_filter/) | `fmc.domains.objects.application_filters` | objects_network.nac.yaml | covered (7 attribute lines) |
| 28 | [AS Path](https://netascode.cisco.com/docs/data_models/fmc/objects/as_path/) | `fmc.domains.objects.as_paths` | objects_routing.nac.yaml | covered (4 attribute lines) |
| 29 | [BFD Teamplate](https://netascode.cisco.com/docs/data_models/fmc/objects/bfd_template/) | `fmc.domains.objects.bfd_templates` | objects_routing.nac.yaml | covered (11 attribute lines) |
| 30 | [Certificate Enrollment](https://netascode.cisco.com/docs/data_models/fmc/objects/certificate_enrollment/) | `fmc.domains.objects.certificate_enrollments` | objects_vpn_pki.nac.yaml | covered (52 attribute lines) |
| 31 | [Certificate Map](https://netascode.cisco.com/docs/data_models/fmc/objects/certificate_map/) | `fmc.domains.objects.certificate_maps` | objects_vpn_pki.nac.yaml | covered (5 attribute lines) |
| 32 | [DNS Server Group](https://netascode.cisco.com/docs/data_models/fmc/objects/dns_server_group/) | `fmc.domains.objects.dns_server_groups` | objects_routing.nac.yaml | covered (5 attribute lines) |
| 33 | [Dynamic Object](https://netascode.cisco.com/docs/data_models/fmc/objects/dynamic_object/) | `fmc.domains.objects.dynamic_objects` | objects_network.nac.yaml | covered (4 attribute lines) |
| 34 | [Expanded Community List](https://netascode.cisco.com/docs/data_models/fmc/objects/expanded_community_list/) | `fmc.domains.objects.expanded_community_lists` | objects_routing.nac.yaml | covered (3 attribute lines) |
| 35 | [Extended Access List](https://netascode.cisco.com/docs/data_models/fmc/objects/extended_access_list/) | `fmc.domains.objects.extended_access_lists` | objects_routing.nac.yaml | covered (18 attribute lines) |
| 36 | [Extended Community List](https://netascode.cisco.com/docs/data_models/fmc/objects/extended_community_list/) | `fmc.domains.objects.extended_community_lists` | objects_routing.nac.yaml | covered (5 attribute lines) |
| 37 | [External Certificate](https://netascode.cisco.com/docs/data_models/fmc/objects/external_certificate/) | `fmc.domains.objects.external_certificates` | objects_vpn_pki.nac.yaml | covered (3 attribute lines) |
| 38 | [FQDN](https://netascode.cisco.com/docs/data_models/fmc/objects/fqdn/) | `fmc.domains.objects.fqdns` | objects_network.nac.yaml | covered (9 attribute lines) |
| 39 | [Geolocation](https://netascode.cisco.com/docs/data_models/fmc/objects/geolocation/) | `fmc.domains.objects.geolocations` | objects_network.nac.yaml | covered (3 attribute lines) |
| 40 | [Group Policy](https://netascode.cisco.com/docs/data_models/fmc/objects/group_policy/) | `fmc.domains.objects.group_policies` | objects_vpn_pki.nac.yaml | covered (43 attribute lines) |
| 41 | [Host](https://netascode.cisco.com/docs/data_models/fmc/objects/host/) | `fmc.domains.objects.hosts` | objects_network.nac.yaml | covered (8 attribute lines) |
| 42 | [ICMPv4](https://netascode.cisco.com/docs/data_models/fmc/objects/icmpv4/) | `fmc.domains.objects.icmpv4s` | objects_network.nac.yaml | covered (5 attribute lines) |
| 43 | [ICMPv6](https://netascode.cisco.com/docs/data_models/fmc/objects/icmpv6/) | `fmc.domains.objects.icmpv6s` | objects_network.nac.yaml | covered (5 attribute lines) |
| 44 | [IKEv1 IPSec Proposal](https://netascode.cisco.com/docs/data_models/fmc/objects/ikev1_ipsec_proposal/) | `fmc.domains.objects.ikev1_ipsec_proposals` | objects_vpn_pki.nac.yaml | covered (4 attribute lines) |
| 45 | [IKEv1 Policy](https://netascode.cisco.com/docs/data_models/fmc/objects/ikev1_policy/) | `fmc.domains.objects.ikev1_policies` | objects_vpn_pki.nac.yaml | covered (8 attribute lines) |
| 46 | [IKEv2 IPSec Proposal](https://netascode.cisco.com/docs/data_models/fmc/objects/ikev2_ipsec_proposal/) | `fmc.domains.objects.ikev2_ipsec_proposals` | objects_vpn_pki.nac.yaml | covered (4 attribute lines) |
| 47 | [IKEv2 Policy](https://netascode.cisco.com/docs/data_models/fmc/objects/ikev2_policy/) | `fmc.domains.objects.ikev2_policies` | objects_vpn_pki.nac.yaml | covered (8 attribute lines) |
| 48 | [Interface Group](https://netascode.cisco.com/docs/data_models/fmc/objects/interface_group/) | `fmc.domains.objects.interface_groups` | objects_network.nac.yaml | covered (2 attribute lines) |
| 49 | [Internal Certificate](https://netascode.cisco.com/docs/data_models/fmc/objects/internal_certificate/) | `fmc.domains.objects.internal_certificates` | objects_vpn_pki.nac.yaml | covered (6 attribute lines) |
| 50 | [Internal Certificate Authority](https://netascode.cisco.com/docs/data_models/fmc/objects/internal_certificate_authority/) | `fmc.domains.objects.internal_certificate_authorities` | objects_vpn_pki.nac.yaml | covered (6 attribute lines) |
| 51 | [IPv4 Address Pool](https://netascode.cisco.com/docs/data_models/fmc/objects/ipv4_address_pool/) | `fmc.domains.objects.ipv4_address_pools` | objects_vpn_pki.nac.yaml | covered (5 attribute lines) |
| 52 | [IPv4 Prefix List](https://netascode.cisco.com/docs/data_models/fmc/objects/ipv4_prefix_list/) | `fmc.domains.objects.ipv4_prefix_lists` | objects_routing.nac.yaml | covered (5 attribute lines) |
| 53 | [IPv6 Address Pool](https://netascode.cisco.com/docs/data_models/fmc/objects/ipv6_address_pool/) | `fmc.domains.objects.ipv6_address_pools` | objects_vpn_pki.nac.yaml | covered (5 attribute lines) |
| 54 | [IPv6 Prefix List](https://netascode.cisco.com/docs/data_models/fmc/objects/ipv6_prefix_list/) | `fmc.domains.objects.ipv6_prefix_lists` | objects_routing.nac.yaml | covered (5 attribute lines) |
| 55 | [Network](https://netascode.cisco.com/docs/data_models/fmc/objects/network/) | `fmc.domains.objects.networks` | objects_network.nac.yaml | covered (8 attribute lines) |
| 56 | [Network Group](https://netascode.cisco.com/docs/data_models/fmc/objects/network_group/) | `fmc.domains.objects.network_groups` | objects_network.nac.yaml | covered (10 attribute lines) |
| 57 | [Policy List](https://netascode.cisco.com/docs/data_models/fmc/objects/policy_list/) | `fmc.domains.objects.policy_lists` | objects_routing.nac.yaml | covered (15 attribute lines) |
| 58 | [Port](https://netascode.cisco.com/docs/data_models/fmc/objects/port/) | `fmc.domains.objects.ports` | objects_network.nac.yaml | covered (5 attribute lines) |
| 59 | [Port Group](https://netascode.cisco.com/docs/data_models/fmc/objects/port_group/) | `fmc.domains.objects.port_groups` | objects_network.nac.yaml | covered (4 attribute lines) |
| 60 | [RADIUS Server Group](https://netascode.cisco.com/docs/data_models/fmc/objects/radius_server_group/) | `fmc.domains.objects.radius_server_groups` | objects_vpn_pki.nac.yaml | covered (18 attribute lines) |
| 61 | [Range](https://netascode.cisco.com/docs/data_models/fmc/objects/range/) | `fmc.domains.objects.ranges` | objects_network.nac.yaml | covered (8 attribute lines) |
| 62 | [Resource Profile](https://netascode.cisco.com/docs/data_models/fmc/objects/resource_profile/) | `fmc.domains.objects.resource_profiles` | objects_network.nac.yaml | covered (3 attribute lines) |
| 63 | [Route Map](https://netascode.cisco.com/docs/data_models/fmc/objects/route_map/) | `fmc.domains.objects.route_maps` | objects_routing.nac.yaml | covered (51 attribute lines) |
| 64 | [Secure Client](https://netascode.cisco.com/docs/data_models/fmc/objects/secure_client/) | `fmc.domains.objects.secure_client_images`<br>`fmc.domains.objects.secure_client_profiles`<br>`fmc.domains.objects.secure_client_posture_packages`<br>`fmc.domains.objects.secure_client_external_browser_packages`<br>`fmc.domains.objects.secure_client_customizations`<br>`fmc.domains.objects.secure_client_custom_attributes` | objects_vpn_pki.nac.yaml | covered (32 attribute lines) |
| 65 | [Security Zone](https://netascode.cisco.com/docs/data_models/fmc/objects/security_zone/) | `fmc.domains.objects.security_zones` | objects_network.nac.yaml | covered (2 attribute lines) |
| 66 | [Service Access](https://netascode.cisco.com/docs/data_models/fmc/objects/service_access/) | `fmc.domains.objects.service_accesses` | objects_vpn_pki.nac.yaml | covered (5 attribute lines) |
| 67 | [Security Group Tag (SGT)](https://netascode.cisco.com/docs/data_models/fmc/objects/sgt/) | `fmc.domains.objects.sgts` | objects_network.nac.yaml | covered (3 attribute lines) |
| 68 | [Single Sign On Server (SSO)](https://netascode.cisco.com/docs/data_models/fmc/objects/single_sign_on_server/) | `fmc.domains.objects.single_sign_on_servers` | objects_vpn_pki.nac.yaml | covered (11 attribute lines) |
| 69 | [Standard Access List](https://netascode.cisco.com/docs/data_models/fmc/objects/standard_access_list/) | `fmc.domains.objects.standard_access_lists` | objects_routing.nac.yaml | covered (4 attribute lines) |
| 70 | [Standard Community List](https://netascode.cisco.com/docs/data_models/fmc/objects/standard_community_list/) | `fmc.domains.objects.standard_community_lists` | objects_routing.nac.yaml | covered (6 attribute lines) |
| 71 | [Time Range](https://netascode.cisco.com/docs/data_models/fmc/objects/time_range/) | `fmc.domains.objects.time_ranges` | objects_network.nac.yaml | covered (12 attribute lines) |
| 72 | [Trusted Certificate Authority](https://netascode.cisco.com/docs/data_models/fmc/objects/trusted_certificate_authority/) | `fmc.domains.objects.trusted_certificate_authorities` | objects_vpn_pki.nac.yaml | covered (3 attribute lines) |
| 73 | [Tunnel Zone](https://netascode.cisco.com/docs/data_models/fmc/objects/tunnel_zone/) | `fmc.domains.objects.tunnel_zones` | objects_network.nac.yaml | covered (2 attribute lines) |
| 74 | [URL](https://netascode.cisco.com/docs/data_models/fmc/objects/url/) | `fmc.domains.objects.urls` | objects_network.nac.yaml | covered (4 attribute lines) |
| 75 | [URL Group](https://netascode.cisco.com/docs/data_models/fmc/objects/url_group/) | `fmc.domains.objects.url_groups` | objects_network.nac.yaml | covered (5 attribute lines) |
| 76 | [VLAN Tag](https://netascode.cisco.com/docs/data_models/fmc/objects/vlan_tag/) | `fmc.domains.objects.vlan_tags` | objects_network.nac.yaml | covered (5 attribute lines) |
| 77 | [VLAN Tag Group](https://netascode.cisco.com/docs/data_models/fmc/objects/vlan_tag_group/) | `fmc.domains.objects.vlan_tag_groups` | objects_network.nac.yaml | covered (6 attribute lines) |
| 78 | [Overview](https://netascode.cisco.com/docs/data_models/fmc/overview/) | - | - | n/a (non-model page) |
| 79 | [Access Control Policy](https://netascode.cisco.com/docs/data_models/fmc/policies/access_control_policy/) | `fmc.domains.policies.access_control_policies` | policies_access_control.nac.yaml | covered (60 attribute lines) |
| 80 | [Marware and File Policy](https://netascode.cisco.com/docs/data_models/fmc/policies/file_policy/) | `fmc.domains.policies.file_policies` | policies_threat.nac.yaml | covered (16 attribute lines) |
| 81 | [FTD NAT Policy](https://netascode.cisco.com/docs/data_models/fmc/policies/ftd_nat_policy/) | `fmc.domains.policies.ftd_nat_policies` | policies_nat.nac.yaml | covered (54 attribute lines) |
| 82 | [Health Policy](https://netascode.cisco.com/docs/data_models/fmc/policies/health_policy/) | `fmc.domains.policies.health_policies` | policies_health.nac.yaml | covered (18 attribute lines) |
| 83 | [Intrusion Policy](https://netascode.cisco.com/docs/data_models/fmc/policies/intrusion_policy/) | `fmc.domains.policies.intrusion_policies` | policies_threat.nac.yaml | covered (4 attribute lines) |
| 84 | [Network Analysis Policy](https://netascode.cisco.com/docs/data_models/fmc/policies/network_analysis_policy/) | `fmc.domains.policies.network_analysis_policies` | policies_threat.nac.yaml | covered (4 attribute lines) |
| 85 | [Prefilter Policy](https://netascode.cisco.com/docs/data_models/fmc/policies/prefilter_policy/) | `fmc.domains.policies.prefilter_policies` | policies_prefilter.nac.yaml | covered (40 attribute lines) |
| 86 | [Deployment](https://netascode.cisco.com/docs/data_models/fmc/system/deployment/) | `fmc.system.deployment` | system.nac.yaml | covered (2 attribute lines) |
| 87 | [Policy Assignment](https://netascode.cisco.com/docs/data_models/fmc/system/policy_assignment/) | `fmc.system.policy_assignment` | system.nac.yaml | covered (2 attribute lines) |
| 88 | [Smart License](https://netascode.cisco.com/docs/data_models/fmc/system/smart_license/) | `fmc.system.smart_license` | system.nac.yaml | covered (4 attribute lines) |
| 89 | [Remote Access](https://netascode.cisco.com/docs/data_models/fmc/vpns/remote_access/) | `fmc.domains.vpns.remote_access` | vpns_remote_access.nac.yaml | covered (100 attribute lines) |
| 90 | [Site to Site](https://netascode.cisco.com/docs/data_models/fmc/vpns/site_to_site/) | `fmc.domains.vpns.site_to_site` | vpns_site_to_site.nac.yaml | covered (79 attribute lines) |

Schema attribute coverage: 1710/1710 distinct attribute paths of `fmc:` (recursive `children` collapsed) are present in the templates; 0 missing.

## Environment variables referenced by `!env` tags

| Variable | Used at |
|---|---|
| `FMC_AREAS_VIRTUAL_LINKS_AUTHENTICATION_AREA_PASSWORD` | `fmc.domains.devices.devices.vrfs.ospfs.areas.virtual_links.authentication_area_password` |
| `FMC_AREAS_VIRTUAL_LINKS_AUTHENTICATION_PASSWORD` | `fmc.domains.devices.devices.vrfs.ospfs.areas.virtual_links.authentication_password` |
| `FMC_BGP_IPV4_NEIGHBORS_AUTHENTICATION_PASSWORD` | `fmc.domains.devices.devices.vrfs.bgp.ipv4_neighbors.authentication_password` |
| `FMC_CERTIFICATE_ENROLLMENTS_EST_PASSWORD` | `fmc.domains.objects.certificate_enrollments.est.password` |
| `FMC_CERTIFICATE_ENROLLMENTS_PKCS12_PASSPHRASE` | `fmc.domains.objects.certificate_enrollments.pkcs12.passphrase` |
| `FMC_CERTIFICATE_ENROLLMENTS_SCEP_CHALLENGE_PASSWORD` | `fmc.domains.objects.certificate_enrollments.scep.challenge_password` |
| `FMC_CHASSIS_LOGICAL_DEVICES_DEVICE_PASSWORD` | `fmc.domains.devices.chassis.logical_devices.device_password` |
| `FMC_DEVICES_CHASSIS_REGISTRATION_KEY` | `fmc.domains.devices.chassis.registration_key` |
| `FMC_DEVICES_CLUSTERS_CLUSTER_KEY` | `fmc.domains.devices.clusters.cluster_key` |
| `FMC_DEVICES_DEVICES_REGISTRATION_KEY` | `fmc.domains.devices.devices.registration_key` |
| `FMC_DEVICES_HA_PAIRS_ENCRYPTION_KEY` | `fmc.domains.devices.ha_pairs.encryption_key` |
| `FMC_FTD_PLATFORM_SETTINGS_SNMP_READ_COMMUNITY` | `fmc.domains.devices.ftd_platform_settings.snmp.read_community` |
| `FMC_INTEGRATIONS_AD_LDAP_REALMS_AD_JOIN_PASSWORD` | `fmc.domains.integrations.ad_ldap_realms.ad_join_password` |
| `FMC_INTEGRATIONS_AD_LDAP_REALMS_DIRECTORY_PASSWORD` | `fmc.domains.integrations.ad_ldap_realms.directory_password` |
| `FMC_KEY_CHAINS_KEYS_KEY` | `fmc.domains.objects.key_chains.keys.key` |
| `FMC_OBJECTS_BFD_TEMPLATES_AUTHENTICATION_PASSWORD` | `fmc.domains.objects.bfd_templates.authentication_password` |
| `FMC_OBJECTS_INTERNAL_CERTIFICATES_PASSWORD` | `fmc.domains.objects.internal_certificates.password` |
| `FMC_OBJECTS_INTERNAL_CERTIFICATES_PRIVATE_KEY` | `fmc.domains.objects.internal_certificates.private_key` |
| `FMC_OBJECTS_INTERNAL_CERTIFICATE_AUTHORITIES_PASSWORD` | `fmc.domains.objects.internal_certificate_authorities.password` |
| `FMC_OBJECTS_INTERNAL_CERTIFICATE_AUTHORITIES_PRIVATE_KEY` | `fmc.domains.objects.internal_certificate_authorities.private_key` |
| `FMC_OSPF_INTERFACES_AUTHENTICATION_AREA_MD5S_KEY` | `fmc.domains.devices.devices.vrfs.ospf_interfaces.authentication_area_md5s.key` |
| `FMC_OSPF_INTERFACES_AUTHENTICATION_MD5S_KEY` | `fmc.domains.devices.devices.vrfs.ospf_interfaces.authentication_md5s.key` |
| `FMC_RADIUS_SERVER_GROUPS_RADIUS_SERVERS_KEY` | `fmc.domains.objects.radius_server_groups.radius_servers.key` |
| `FMC_REMOTE_ACCESS_LOAD_BALANCING_IPSEC_ENCRYPTION_KEY` | `fmc.domains.vpns.remote_access.load_balancing.ipsec_encryption_key` |
| `FMC_SITE_TO_SITE_IKE_SETTINGS_IKEV1_MANUAL_PRE_SHARED_KEY` | `fmc.domains.vpns.site_to_site.ike_settings.ikev1_manual_pre_shared_key` |
| `FMC_SITE_TO_SITE_IKE_SETTINGS_IKEV2_MANUAL_PRE_SHARED_KEY` | `fmc.domains.vpns.site_to_site.ike_settings.ikev2_manual_pre_shared_key` |
| `FMC_SNMP_MANAGEMENT_HOSTS_READ_COMMUNITY` | `fmc.domains.devices.ftd_platform_settings.snmp.management_hosts.read_community` |
| `FMC_SNMP_SNMPV3_USERS_AUTHENTICATION_PASSWORD` | `fmc.domains.devices.ftd_platform_settings.snmp.snmpv3_users.authentication_password` |
| `FMC_SNMP_SNMPV3_USERS_ENCRYPTION_PASSWORD` | `fmc.domains.devices.ftd_platform_settings.snmp.snmpv3_users.encryption_password` |
| `FMC_SYSLOG_LOGGING_SETUP_FTP_SERVER_PASSWORD` | `fmc.domains.devices.ftd_platform_settings.syslog.logging_setup.ftp_server_password` |
| `FMC_SYSTEM_SMART_LICENSE_TOKEN` | `fmc.system.smart_license.token` |
| `FMC_VIRTUAL_LINKS_AUTHENTICATION_AREA_MD5S_KEY` | `fmc.domains.devices.devices.vrfs.ospfs.areas.virtual_links.authentication_area_md5s.key` |
| `FMC_VIRTUAL_LINKS_AUTHENTICATION_MD5S_KEY` | `fmc.domains.devices.devices.vrfs.ospfs.areas.virtual_links.authentication_md5s.key` |
| `FMC_VRFS_ETHERCHANNEL_INTERFACES_IPV4_PPPOE_PASSWORD` | `fmc.domains.devices.devices.vrfs.etherchannel_interfaces.ipv4_pppoe_password` |
| `FMC_VRFS_OSPF_INTERFACES_AUTHENTICATION_AREA_PASSWORD` | `fmc.domains.devices.devices.vrfs.ospf_interfaces.authentication_area_password` |
| `FMC_VRFS_OSPF_INTERFACES_AUTHENTICATION_PASSWORD` | `fmc.domains.devices.devices.vrfs.ospf_interfaces.authentication_password` |
| `FMC_VRFS_PHYSICAL_INTERFACES_IPV4_PPPOE_PASSWORD` | `fmc.domains.devices.devices.vrfs.physical_interfaces.ipv4_pppoe_password` |
| `FMC_VRFS_SUB_INTERFACES_IPV4_PPPOE_PASSWORD` | `fmc.domains.devices.devices.vrfs.sub_interfaces.ipv4_pppoe_password` |

## Validation performed (2026-10-27)

| Check | Result |
|---|---|
| Merged `data/*.nac.yaml` vs netascode/schema `schema.json` (Draft 2020-12, `additionalProperties: false`) | 0 errors |
| Same, with every `#~` alternative uncommented (`--full`) | 0 errors |
| Real `provider::utils::yaml_merge` (netascode/utils 2.0.0, `!env` resolved) output vs schema | 0 errors; identical to the Python merge used by the validator |
| Light reference checks (zones, network/port objects, intrusion policy, ACP/NAT on devices, HA members) | 0 errors |
| `terraform fmt -check`, `terraform init`, `terraform validate` | success |
| `terraform plan/apply` | **not run** - would require contacting an FMC (out of scope) |

## Gaps, caveats and assumptions

- **Not modelled by NaC FMC** (no docs page and no schema key): SSL/Decryption policy, DNS policy, Identity policy, QoS, FlexConfig, PBR, EIGRP/IS-IS, threat-defense service policy. `policies_threat.nac.yaml` therefore covers Intrusion, Network Analysis and Malware & File only.
- **Docs vs schema:** the ACP page lists `access_rules.source_port_literals.icmp_type/icmp_code`, which the schema rejects - omitted. The schema caps ICMPv6 `icmp_type` at 41 (echo-request 128 is rejected), so the ICMPv6 example uses type 1.
- **Schema (main) is ahead of module 0.1.3:** keys marked `WARN: not referenced by nac-fmc 0.1.3` (OSPF `ospfs`/`ospf_interfaces`, SLA monitors, key chains, sinkholes, cipher-suite lists, distinguished names, MAC address pools, `existing` FQDN groups, `deploy_on_destroy`, RA-VPN `ipv4_use_dhcp`, ...) validate but are ignored by the released module.
- **Module 0.1.3 observation:** in `fmc_policies.tf` the manual-NAT `original_source_port_id` is resolved from `translated_source_port` (so `original_source_port` is ignored) - check before relying on port-translated manual NAT.
- Templates intentionally combine things a real deployment would not (one device that is also in an HA pair, a cluster and a chassis; every logging option on). They are schema-valid, not a design.
- `existing.nac.yaml` uses built-in FMC object names where they exist (e.g. `IPv4-Private-All-RFC1918`, `Balanced Security and Connectivity`, `Default Prefilter Policy`, `Initial_Health_Policy`, `CiscoUmbrellaDNSServerGroup`); other `*_LEGACY` names are placeholders for objects owned elsewhere. Do not define the same name under both `fmc:` and `existing:`.
- Values for attributes the docs don't exemplify are realistic placeholders chosen by type/name; review enums against your FMC version.
