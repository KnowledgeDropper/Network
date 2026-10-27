# SD-Access

Configuration templates for Cisco SD-Access.

Use this folder for fabric templates: underlay routing, edge and border node configuration, control-plane nodes, and the host-onboarding pieces that go with a Catalyst Center fabric. Keep device-specific values as placeholders. Do not store DNA Center or Catalyst Center credentials, IP transit keys, or LISP/BGP authentication secrets in this tree.

The IOS-XE base template in `../IOS-XE/` is a management baseline, not a fabric node configuration. SD-Access edge ports need CDP or LLDP for endpoint and access-point discovery, so do not reuse the untrusted-edge neighbor-discovery stanza from that baseline on fabric edges.

The Catalyst Center Network as Code model, including fabric sites, virtual networks, transits, and border devices, is in [`../Network-as-Code/templates/catalyst_center/`](../Network-as-Code/templates/catalyst_center/). Those files are schema references for `netascode/nac-catalystcenter/catalystcenter` 0.5.1. Copy the sections you need; do not apply the whole tree.
