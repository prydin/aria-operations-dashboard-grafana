import json
from typing import Iterable

version = "1.0.0"


def recurse_replace(node):
    if not (isinstance(node, dict) or isinstance(node, tuple) or isinstance(node, list)):
        return
    if "datasource" in node:
        datasource = node["datasource"]
        if datasource["type"] == "vmware-ariaoperations-datasource":
            datasource['uid'] = "${DS_ARIAOPS_ID}"
    if isinstance(node, dict):
        for child in node:
            recurse_replace(node[child])
    elif isinstance(node, tuple) or isinstance(node, list):
        for child in node:
            recurse_replace(child)


with open('aria-ops-dashboard.json', 'r') as f:
    dashboard = json.load(f)
dashboard["__inputs"] = {
    "name": "DS_ARIAOPS_ID",
    "label": "Aria Ops Source",
    "description": "",
    "type": "datasource",
    "pluginId": "vmware-ariaoperations-datasource",
    "pluginName": "VMWare Aria Operations"
}

recurse_replace(dashboard)

with open(f"aria-ops-dashboard-{version}.json", 'w') as f:
    json.dump(dashboard, f, indent=2)
