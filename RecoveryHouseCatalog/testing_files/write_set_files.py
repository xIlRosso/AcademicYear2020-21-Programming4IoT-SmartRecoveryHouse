# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 19:36:12 2021

@author: ilros
"""
import requests

import json


with open('Regression_Trained.json') as json_in:
    data=json.load(json_in)


r=requests.post('http://localhost:8080/trained_models/', json=data)


rr=requests.get('http://localhost:8080/trained_models/')
datum=rr.json()

print(datum)