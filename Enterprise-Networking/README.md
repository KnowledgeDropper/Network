# Enterprise Networking

Configuration templates for enterprise networking. Copy a template, replace every placeholder, and apply it on a device. These files are not running configurations and they do not contain secrets.

## Folder index

| Folder | Purpose |
| --- | --- |
| [IOS-XE](IOS-XE/) | Configuration templates for Cisco IOS-XE. |
| [IOS-XR](IOS-XR/) | Configuration templates for Cisco IOS-XR. |
| [SD-Access](SD-Access/) | Configuration templates for Cisco SD-Access. |
| [SD-WAN](SD-WAN/) | Configuration templates for Cisco SD-WAN. |

IOS-XE and IOS-XR each include a hardened base template. SD-Access and SD-WAN are reserved for templates of those designs. Do not paste an IOS-XE template into IOS-XR, or the reverse. The command models differ, including AAA, SSH, logging, SNMP, and the IOS-XR commit model.
