#!/usr/bin/env python3
"""Gera a tabela de badges 'Add to your instance' a partir dos source_url."""
import pathlib, re, urllib.parse, sys

class L: pass
base = pathlib.Path(__file__).resolve().parent.parent
rows = []
for p in sorted((base / "blueprints/automation/rickard2014").glob("*.yaml")):
    t = p.read_text()
    src = re.search(r"^\s*source_url:\s*(\S+)", t, re.M)
    name = re.search(r"^\s*name:\s*(.+)$", t, re.M)
    if not src:
        print(f"AVISO: {p.name} sem source_url", file=sys.stderr); continue
    url = src.group(1)
    my = "https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=" + \
         urllib.parse.quote(url, safe="")
    rows.append((p.name, (name.group(1).strip() if name else p.stem), my))

print("| Blueprint | Nome no HA | Instalar |")
print("|---|---|---|")
for fn, nm, my in rows:
    print(f"| `{fn}` | {nm} | [![Add to your Home Assistant]"
          f"(https://my.home-assistant.io/badges/blueprint_import.svg)]({my}) |")
