#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 09:50:14 2023

@author: michael
"""

import xml.etree.ElementTree as ET
import carla

routes = ET.parse('leaderboard/data/training_routes/routes_town01_short.xml').getroot()

WEATHERS = {
    "ClearNoon": carla.WeatherParameters.ClearNoon,
    "ClearSunset": carla.WeatherParameters.ClearSunset,
    "CloudyNoon": carla.WeatherParameters.CloudyNoon,
    "CloudySunset": carla.WeatherParameters.CloudySunset,
    "WetNoon": carla.WeatherParameters.WetNoon,
    "WetSunset": carla.WeatherParameters.WetSunset,
    "MidRainyNoon": carla.WeatherParameters.MidRainyNoon,
    "MidRainSunset": carla.WeatherParameters.MidRainSunset,
    "WetCloudyNoon": carla.WeatherParameters.WetCloudyNoon,
    "WetCloudySunset": carla.WeatherParameters.WetCloudySunset,
    "HardRainNoon": carla.WeatherParameters.HardRainNoon,
    "HardRainSunset": carla.WeatherParameters.HardRainSunset,
    "SoftRainNoon": carla.WeatherParameters.SoftRainNoon,
    "SoftRainSunset": carla.WeatherParameters.SoftRainSunset,
    "ClearNight": carla.WeatherParameters(5.0,0.0,0.0,10.0,-1.0,-90.0,60.0,75.0,1.0,0.0),
    "CloudyNight": carla.WeatherParameters(60.0,0.0,0.0,10.0,-1.0,-90.0,60.0,0.75,0.1,0.0),
    "WetNight": carla.WeatherParameters(5.0,0.0,50.0,10.0,-1.0,-90.0,60.0,75.0,1.0,60.0),
    "WetCloudyNight": carla.WeatherParameters(60.0,0.0,50.0,10.0,-1.0,-90.0,60.0,0.75,0.1,60.0),
    "SoftRainNight": carla.WeatherParameters(60.0,30.0,50.0,30.0,-1.0,-90.0,60.0,0.75,0.1,60.0),
    "MidRainyNight": carla.WeatherParameters(80.0,60.0,60.0,60.0,-1.0,-90.0,60.0,0.75,0.1,80.0),
    "HardRainNight": carla.WeatherParameters(100.0,100.0,90.0,100.0,-1.0,-90.0,100.0,0.75,0.1,100.0),
}
WEATHERS_IDS = list(WEATHERS)

new_routes = ET.Element('routes')
route_id = 0
for w in WEATHERS_IDS:
    new_routes.append(ET.Comment(w))
    weather = WEATHERS[w]
    weather_dict = {k: str(getattr(weather, k)) for k in dir(weather) if not k.startswith("__") and isinstance(getattr(weather, k), float)}
    weather_dict['id'] = w
    for route in routes:
        weather_element = ET.Element('weather')
        for k, v in weather_dict.items():
            weather_element.set(k, v)
        new_route = ET.Element('route')
        new_route.set("town", "Town01")
        new_route.set("id", str(route_id))
        route_id += 1
        for waypoint in route:
            weather_element.append(waypoint)
        new_route.append(weather_element)
        new_routes.append(new_route)

with open("weather_routes_town01_short.xml", 'w') as f:
    print(ET.tostring(new_routes).decode(), file=f)
