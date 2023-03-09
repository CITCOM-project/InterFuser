#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 09:32:32 2022

@author: michael
"""

import pandas as pd
import json
import re
import sys
import carla

# RESULTS_FILE = "data/CITCoM_data_collect_town01_results/data_collect_town01_results.json"
RESULTS_FILE = sys.argv[1]

collision_re = re.compile(r"Agent collided against object with type=\w+\.[\w-]+\.\w+ and id=\d+")
weather_re = re.compile("weather-(\d+)")

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

import sys

RESULTS_FILE = sys.argv[1]

weather_match = weather_re.search(RESULTS_FILE)
weather = None
if weather_match:
    weather_inx = int(weather_match.group(1))
    weather = WEATHERS[WEATHERS_IDS[weather_inx]]

routes = {}

with open(RESULTS_FILE) as f:
    results = json.load(f)

for route in results['_checkpoint']['records']:
    index = int(route.pop("index"))
    if route['weather']:
        weather = route['weather']
    else:
        route['weather'] = {}
        route['weather']["cloudiness"] = weather.cloudiness
        route['weather']["precipitation"] = weather.precipitation
        route['weather']["precipitation_deposits"] = weather.precipitation_deposits
        route['weather']["wind_intensity"] = weather.wind_intensity
        route['weather']["sun_azimuth_angle"] = weather.sun_azimuth_angle
        route['weather']["sun_altitude_angle"] = weather.sun_altitude_angle
        route['weather']["fog_density"] = weather.fog_density
        route['weather']["fog_distance"] = weather.fog_distance
        route['weather']["fog_falloff"] = weather.fog_falloff
        route['weather']["wetness"] = weather.wetness
    for condition in route['weather']:
        route[condition] = route['weather'][condition]
    for infraction in route['infractions']:
        route[infraction] = len(route['infractions'][infraction])
        # if infraction.startswith("collisions_") and len(route['infractions'][infraction]) > 0:
            # ev, ov = get_velocity(route['infractions'][infraction][0])
            # route['collision_ego_velocity'] = ev
            # route['collision_other_velocity'] = ov
    for meta in route['meta']:
        route[meta] = route['meta'][meta]
    for score in route['scores']:
        route[score] = route['scores'][score]
    route.pop('weather')
    route.pop('infractions')
    # route.pop('friction')
    route.pop('meta')
    route.pop('scores')
    routes[index] = route

# print(routes)

data = pd.DataFrame.from_dict(routes, orient="index")#.dropna()
# for col in data:
#     if len(set(data[col])) == 1:
#         data.drop(col, axis=1, inplace=True)


data.to_csv(RESULTS_FILE.replace(".json", ".csv"))
print(len(data), "data points")
print(data['collisions_vehicle'].sum(), "Vehicle collisions")
