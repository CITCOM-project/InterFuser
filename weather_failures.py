#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 09:46:15 2023

@author: michael
"""

import json
import xml.etree.ElementTree as ET

routes = ET.parse('leaderboard/data/training_routes/failed_routes.xml').getroot()

with open("dataset_failed_lincoln/TCP_failed/results/routes_town01_short.json") as f:
    results = json.load(f)

assert len(results['_checkpoint']['records']) == len(routes), "MISMATCH"

for result, route in zip(results['_checkpoint']['records'], routes):
    result['weather'] = {k: (v if k == "id" else float(v)) for k, v in route[0].attrib.items()}

with open("dataset_failed_lincoln/TCP_failed/results/routes_town01_short_weather.json", 'w') as f:
    json.dump(results, f, indent=2)