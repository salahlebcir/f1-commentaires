#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 14 18:45:01 2025

@author: slebcir
"""

import requests

params = {
    "type": "tour",
    "gp": "Bahrain Grand Prix",
    "cible": "10"
}

r = requests.get("https://f1-commentaires.onrender.com/comments", params=params)
print("Commentaires :")
print(r.json())
