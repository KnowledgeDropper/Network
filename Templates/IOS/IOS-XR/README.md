# IOS-XR Configuration Templates

This folder contains configuration templates for Cisco IOS-XR platforms, including
ASR 9000, NCS 5500/5700, and Cisco 8000 series routers.

Templates here are intended as starting points for demos, labs, and customer-facing
deliverables within the Cisco CX US Public Sector practice. All templates use
placeholder values and do not reflect real customer configurations.

## Platforms Covered
- ASR 9000 series
- NCS 5500 / 5700 series
- Cisco 8000 series

## Usage
Replace all placeholder values (e.g., `[HOSTNAME]`, `[IP ADDRESS]`) before
applying any template to a device. IOS-XR uses a commit/rollback model —
always review staged changes with `show commit changes diff` before committing.
Validate in a lab environment first.
