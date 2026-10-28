# Network-as-Code templates: `hyperfabric`

Generated from https://netascode.cisco.com/docs/data_models/hyperfabric/ (crawled 2026-10-27). One template per data-model page; each carries inline comments with type, constraint, default and required flag.

8 templates.

| Template | Model | Source |
|---|---|---|
| [fabric/connection.nac.yaml](fabric/connection.nac.yaml) | Connection | https://netascode.cisco.com/docs/data_models/hyperfabric/fabric/connection/ |
| [fabric/fabric.nac.yaml](fabric/fabric.nac.yaml) | Fabric | https://netascode.cisco.com/docs/data_models/hyperfabric/fabric/fabric/ |
| [fabric/loopback.nac.yaml](fabric/loopback.nac.yaml) | Loopback | https://netascode.cisco.com/docs/data_models/hyperfabric/fabric/loopback/ |
| [fabric/node.nac.yaml](fabric/node.nac.yaml) | Node | https://netascode.cisco.com/docs/data_models/hyperfabric/fabric/node/ |
| [fabric/port.nac.yaml](fabric/port.nac.yaml) | Port | https://netascode.cisco.com/docs/data_models/hyperfabric/fabric/port/ |
| [fabric/vni.nac.yaml](fabric/vni.nac.yaml) | VNI | https://netascode.cisco.com/docs/data_models/hyperfabric/fabric/vni/ |
| [fabric/vrf.nac.yaml](fabric/vrf.nac.yaml) | VRF | https://netascode.cisco.com/docs/data_models/hyperfabric/fabric/vrf/ |
| [system/user.nac.yaml](system/user.nac.yaml) | User | https://netascode.cisco.com/docs/data_models/hyperfabric/system/user/ |


## Validation (2026-10-27)

- YAML parse (PyYAML safe_load + duplicate-key check): 8 pass / 0 fail
- `nac-validate` v2.0.0, syntax-only mode (no Yamale schema for this tech is published): PASSED
- Keys checked against the scraped data-model tables: 8 pass / 0 fail
- JSON Schema (python jsonschema, Draft 2020-12, netascode/schema@7334e34): 8 pass / 0 fail. Every failure is a key or type that netascode.cisco.com documents but the published schema doesn't contain. Those keys are tagged inline with `NOTE: documented on page but not in published NaC JSON schema`.
- Keys tagged `required by official NaC JSON schema ... not listed on this page` were added because the schema requires them on a parent object (for example a parent `name`) that the page leaves out.
