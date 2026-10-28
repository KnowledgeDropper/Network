#!/usr/bin/env python3
"""Offline pre-flight checks for NaC template YAML (FMC or ISE).

1. Loads every data/*.yaml (and defaults/*.yaml if present); `!env VAR` tags resolve to "${VAR}" placeholders.
2. Deep-merges them like netascode/utils yaml_merge (maps deep-merged; list items merged when all their
   primitive values are equal, e.g. `- name: Global`).
3. Validates the merged model against the published Network-as-Code JSON Schema
   (https://github.com/netascode/schema/blob/main/schema.json).
4. With --full, also validates the model with every "#~" (commented-out mutually exclusive alternative) line
   re-enabled, so alternatives are guaranteed schema-valid as well.
5. Light referential checks (names referenced in common reference fields must be defined in the templates
   or under existing:).

Usage:
  python3 -m venv .venv && .venv/bin/pip install jsonschema pyyaml
  .venv/bin/python ../scripts/validate_schema.py [--full] [--schema schema.json] [dir]   # dir defaults to "."
"""
import argparse, glob, json, os, re, sys, urllib.request
import jsonschema, yaml

SCHEMA_URL = "https://raw.githubusercontent.com/netascode/schema/main/schema.json"


class Loader(yaml.SafeLoader):
    pass


Loader.add_constructor('!env', lambda l, n: os.environ.get(l.construct_scalar(n), 'changeme'))  # unset -> short dummy (some secrets have maxLength 8)


def prims(d):
    return {k: v for k, v in d.items() if not isinstance(v, (dict, list))}


def merge(a, b):
    if isinstance(a, dict) and isinstance(b, dict):
        for k, v in b.items():
            a[k] = merge(a[k], v) if k in a else v
        return a
    if isinstance(a, list) and isinstance(b, list):
        for item in b:
            m = [x for x in a if isinstance(x, dict) and isinstance(item, dict) and prims(x) == prims(item)] \
                if isinstance(item, dict) and prims(item) else []
            merge(m[0], item) if m else a.append(item)
        return a
    return b


def load(d, full):
    model = {}
    files = sorted(glob.glob(f"{d}/data/*.y*ml") + glob.glob(f"{d}/defaults/*.y*ml"))
    for f in files:
        txt = open(f).read()
        if full:
            txt = re.sub(r'^(\s*)#~ ', r'\1', txt, flags=re.M)
        merge(model, yaml.load(txt, Loader=Loader) or {})
    return model, files


def collect(node, path, out):
    """path-keyed index of names: 'fmc.domains.objects.hosts' -> {names}"""
    if isinstance(node, dict):
        for k, v in node.items():
            collect(v, path + (k,), out)
    elif isinstance(node, list):
        for x in node:
            if isinstance(x, dict) and 'name' in x:
                out.setdefault('.'.join(p for p in path if p not in ('existing',)), set()).add(x['name'])
            collect(x, path, out)


def walk_refs(node, path, out):
    if isinstance(node, dict):
        for k, v in node.items():
            walk_refs(v, path + (k,), out)
    elif isinstance(node, list):
        if node and all(not isinstance(x, (dict, list)) for x in node):
            for x in node:
                out.append((path, x))
        else:
            for x in node:
                walk_refs(x, path, out)
    else:
        out.append((path, node))


O = 'fmc.domains.objects.'
REF_RULES = {
    'fmc': [
        (r'(source|destination)_zones$', [O + 'security_zones']),
        (r'(source|destination)_network_objects$|network_groups\.objects$', [O + 'hosts', O + 'networks', O + 'ranges', O + 'fqdns', O + 'network_groups']),
        (r'(source|destination)_port_objects$|port_groups\.objects$', [O + 'ports', O + 'port_groups', O + 'icmpv4s', O + 'icmpv6s']),
        (r'access_rules\.intrusion_policy$', ['fmc.domains.policies.intrusion_policies']),
        (r'devices\.devices\.access_control_policy$', ['fmc.domains.policies.access_control_policies']),
        (r'devices\.devices\.nat_policy$', ['fmc.domains.policies.ftd_nat_policies']),
        (r'(primary|secondary)_device$', ['fmc.domains.devices.devices']),
    ],
    'ise': [
        (r'policy_sets\.service_name$', ['ise.network_access.policy_elements.allowed_protocols', 'ise.device_administration.policy_elements.allowed_protocols']),
        (r'network_access\..*rules\.profiles$', ['ise.network_access.policy_elements.authorization_profiles']),
        (r'device_administration\..*rules\.command_sets$', ['ise.device_administration.policy_elements.tacacs_command_sets']),
        (r'device_administration\..*rules\.profile$', ['ise.device_administration.policy_elements.tacacs_profiles']),
        (r'rules\.security_group$|matrix_entries\.(source|destination)_sgt$|ip_sgt_mappings\.sgt$', ['ise.trust_sec.security_groups']),
        (r'matrix_entries\.sgacl_name$', ['ise.trust_sec.security_group_acls']),
        (r'internal_users\.user_identity_groups$', ['ise.identity_management.user_identity_groups']),
        (r'authorization_profiles\.dacl_name$', ['ise.network_access.policy_elements.downloadable_acls']),
    ],
}
BUILTINS = {'ise': {'Default Network Access', 'Default Device Admin', 'PermitAccess', 'DenyAccess', 'PermitAllCommands',
                    'DenyAllCommands', 'Default Shell Profile', 'Deny All Shell Profile', 'Permit IP', 'Deny IP',
                    'Unknown', 'TrustSec_Devices', 'Employees', 'Guests', 'ANY', 'ALL_ACCOUNTS (default)', 'Employee'}}


def ref_check(tech, model):
    names = {}
    collect(model, (), names)
    refs = []
    walk_refs(model.get(tech, {}), (tech,), refs)
    errs = []
    for path, val in refs:
        p = '.'.join(path)
        for rx, targets in REF_RULES.get(tech, []):
            if re.search(rx, p) and isinstance(val, str) and val != 'changeme':
                pool = set().union(*[names.get(t, set()) for t in targets]) | BUILTINS.get(tech, set())
                if val not in pool:
                    errs.append(f"ref: {p}: '{val}' not defined in {targets}")
    return errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('dir', nargs='?', default='.')
    ap.add_argument('--schema')
    ap.add_argument('--full', action='store_true')
    a = ap.parse_args()
    schema = json.load(open(a.schema)) if a.schema else json.load(urllib.request.urlopen(SCHEMA_URL, timeout=60))
    v = jsonschema.Draft202012Validator(schema)
    total = 0
    for full in ([False, True] if a.full else [False]):
        model, files = load(a.dir, full)
        tech = [k for k in model if k in ('fmc', 'ise')]
        errs = [f"schema: {'/'.join(map(str, e.path))}: {e.message[:300]}" for e in v.iter_errors(model)]
        for t in tech:
            errs += ref_check(t, model)
        label = 'with #~ alternatives enabled' if full else 'active config'
        print(f"[{label}] {len(files)} file(s), top-level keys {sorted(model)}: {len(errs)} problem(s)")
        for e in errs:
            print('  ERROR', e)
        total += len(errs)
    sys.exit(1 if total else 0)


if __name__ == '__main__':
    main()
