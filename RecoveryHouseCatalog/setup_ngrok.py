# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 11:14:23 2021

@author: ilros
"""

from pyngrok import ngrok
from publish_ngrok_addr.publish_methods import Publishers
import json

url = ngrok.connect(8080).public_url

with open('settings.json') as json_in:
    conf=json.load(json_in)
iterations=3600

p=Publishers()

p.run(url, conf["broker"], conf["port"], "programming_for_iot/aa2021/SmartRecoveryHouse/catalog_public_address", iterations)
