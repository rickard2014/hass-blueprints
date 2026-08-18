#!/usr/bin/env python3
"""Valida sintaxe YAML e estrutura mínima de blueprint do Home Assistant."""
import sys, pathlib, yaml

class L(yaml.SafeLoader): pass
L.add_multi_constructor('!input',  lambda l,s,n: f"<input:{s}>")
L.add_multi_constructor('!secret', lambda l,s,n: "<secret>")

root = pathlib.Path(__file__).resolve().parent.parent / "blueprints"
rc = 0
for p in sorted(root.rglob("*.yaml")):
    rel = p.relative_to(root)
    try:
        d = yaml.load(p.read_text(), Loader=L)
    except Exception as e:
        print(f"FAIL  {rel}: YAML inválido: {e}"); rc = 1; continue
    if not isinstance(d, dict) or "blueprint" not in d:
        print(f"FAIL  {rel}: sem bloco 'blueprint'"); rc = 1; continue
    bp = d["blueprint"]
    missing = [k for k in ("name", "domain") if k not in bp]
    if missing:
        print(f"FAIL  {rel}: blueprint sem {missing}"); rc = 1; continue
    expected = rel.parts[0]
    if bp["domain"] != expected:
        print(f"FAIL  {rel}: domain '{bp['domain']}' != pasta '{expected}'"); rc = 1; continue
    print(f"OK    {rel}  [{bp['domain']}] {bp['name']}")
sys.exit(rc)
