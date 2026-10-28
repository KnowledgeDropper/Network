# Enterprise Networking

Configuration templates for enterprise networking. Copy a template, replace every placeholder, and apply it on a device. These files are not running configurations and they do not contain secrets.

## Folder index

| Folder | Purpose |
| --- | --- |
| [IOS-XE](IOS-XE/) | Configuration templates for Cisco IOS-XE. |
| [IOS-XR](IOS-XR/) | Configuration templates for Cisco IOS-XR. |
| [SD-Access](SD-Access/) | Configuration templates for Cisco SD-Access. |
| [SD-WAN](SD-WAN/) | Configuration templates for Cisco SD-WAN. |
| [Network-as-Code](Network-as-Code/) | YAML data models that Terraform pushes to IOS-XE and IOS-XR, plus schema templates for IOS-XE, IOS-XR, Catalyst SD-WAN, Catalyst Center, and Meraki. |

IOS-XE and IOS-XR each include a hardened base template. SD-Access and SD-WAN are reserved for templates of those designs. Do not paste an IOS-XE template into IOS-XR, or the reverse. The command models differ, including AAA, SSH, logging, SNMP, and the IOS-XR commit model.

Network-as-Code is the same baseline as YAML consumed by Terraform. It uses a separate root for each platform. Schema templates for IOS-XE, IOS-XR, Catalyst SD-WAN, Catalyst Center, and Meraki are under [Network-as-Code/templates](Network-as-Code/templates/). See that folder's README for the workflow and for how credentials are supplied. The working IOS-XE and IOS-XR roots still read `data/` only.
