#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 09:57:58 2022

@author: michael
"""
import pandas as pd
import glob

csvs = glob.glob("dataset/weather-*/results/*.csv")

data = pd.concat([pd.read_csv(csv, index_col=0) for csv in csvs])

data.to_csv("dataset/big_data.csv")

print(len(data), "data points")
