#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 18:35:33 2023

@author: svetlanamaslenkova
"""

import requests 
from input_data import data_in

URL = 'http://127.0.0.1:5000/predict'
headers = {"Content-Type": "application/json"}
data = {"input": data_in}

r = requests.get(URL, headers=headers, json=data) 

r.json()