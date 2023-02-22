#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 08:30:13 2023

@author: michael
"""
import xml.etree.ElementTree as ET
import carla
from xml.dom import minidom


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, "utf-8")
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def build_weather(weather, weather_id):
    weather_attr = ET.Element("weather")
    weather_attr.set("id", weather_id)
    for k in weather_attrs:
        weather_attr.set(k, str(getattr(weather, k)))
    return weather_attr


tree = ET.parse("leaderboard/data/training_routes/routes_town01_short.xml")
routes = tree.getroot()

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
    "ClearNight": carla.WeatherParameters(
        5.0, 0.0, 0.0, 10.0, -1.0, -90.0, 60.0, 75.0, 1.0, 0.0
    ),
    "CloudyNight": carla.WeatherParameters(
        60.0, 0.0, 0.0, 10.0, -1.0, -90.0, 60.0, 0.75, 0.1, 0.0
    ),
    "WetNight": carla.WeatherParameters(
        5.0, 0.0, 50.0, 10.0, -1.0, -90.0, 60.0, 75.0, 1.0, 60.0
    ),
    "WetCloudyNight": carla.WeatherParameters(
        60.0, 0.0, 50.0, 10.0, -1.0, -90.0, 60.0, 0.75, 0.1, 60.0
    ),
    "SoftRainNight": carla.WeatherParameters(
        60.0, 30.0, 50.0, 30.0, -1.0, -90.0, 60.0, 0.75, 0.1, 60.0
    ),
    "MidRainyNight": carla.WeatherParameters(
        80.0, 60.0, 60.0, 60.0, -1.0, -90.0, 60.0, 0.75, 0.1, 80.0
    ),
    "HardRainNight": carla.WeatherParameters(
        100.0, 100.0, 90.0, 100.0, -1.0, -90.0, 100.0, 0.75, 0.1, 100.0
    ),
}
WEATHERS_IDS = list(WEATHERS)

weather_attrs = [
    "cloudiness",
    "precipitation",
    "precipitation_deposits",
    "wind_intensity",
    "sun_azimuth_angle",
    "sun_altitude_angle",
    "fog_density",
    "fog_distance",
    "fog_falloff",
    "wetness",
    "scattering_intensity",
    "rayleigh_scattering_scale",
]

weather_routes = ET.Element("routes")

for w in range(14):
    weather_routes.append(ET.Comment(WEATHERS_IDS[w]))
    for route in routes:
        weather = build_weather(WEATHERS[WEATHERS_IDS[w]], WEATHERS_IDS[w])
        weather_route = ET.Element("route")
        weather_route.set("id", route.get("id"))
        weather_route.set("town", route.get("town"))
        for waypoint in route:
            weather.append(waypoint)
        weather_route.append(weather)
        weather_routes.append(weather_route)

with open("leaderboard/data/training_routes/routes_town01_short_weather.xml", 'w') as f:
    print(ET.tostring(weather_routes, "utf-8").decode('utf8'), file=f)
