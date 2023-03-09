#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 09:46:15 2023

@author: michael
"""

import json
import xml.etree.ElementTree as ET
import sys

RESULTS_FILE = sys.argv[1]
ROUTES_FILE = sys.argv[2]

assert RESULTS_FILE.endswith(".json"), "Routes file should be a JSON file"
assert ROUTES_FILE.endswith(".xml"), "Routes file should be an XML file"

routes = ET.parse(ROUTES_FILE).getroot()

with open(RESULTS_FILE) as f:
    results = json.load(f)

assert len(results['_checkpoint']['records']) == len(routes), "MISMATCH"

for result, route in zip(results['_checkpoint']['records'], routes):
    result['weather'] = {k: (v if k == "id" else float(v)) for k, v in route[0].attrib.items()}

print(RESULTS_FILE.replace(".json", "_weather.json"))
with open(RESULTS_FILE.replace(".json", "_weather.json"), 'w') as f:
    json.dump(results, f, indent=2)
