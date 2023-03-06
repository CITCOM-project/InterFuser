#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 11:20:19 2023

@author: michael
"""

import xml.etree.ElementTree as ET

routes = ET.parse('leaderboard/data/training_routes/routes_town01_short.xml').getroot()

for route in routes:
    print(f"({route[0].attrib['x']}, {route[0].attrib['y']}),")
