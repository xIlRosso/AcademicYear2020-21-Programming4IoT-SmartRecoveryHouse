import json
import requests
import time
import numpy as np

class Actuators:
    def __init__(self, data):
        self.types = [] #put the keys here
        self.tresholds = data

    def get_keys(self):
        for keys in self.tresholds:
            self.types.append(keys)

        return self.types


    def sensor_based_actuations(self, idn):
        with open('Time_control_strategies/sens_act.json') as json_in:
            data=json.load(json_in)
        resp={
            "lights" : "",
            "heating" : "",
            "humidifier" : ""            
        }
        #extract sensor values
        values={
            "Temperature" : 0,
            "LuminousIntensity" : 0,
            "Humidity" : 0
        }

        
        
        values[data["devicesList"][0]["e"][0]["n"]]=data["devicesList"][0]["e"][0]["v"]

        if values["Temperature"] < self.tresholds["Temperature"][0]:
            resp["heating"] = "off"
        elif values["Temperature"] > self.tresholds["Temperature"][1]:
            resp["heating"] = "on"
        if values["LuminousIntensity"] < self.tresholds["LuminousIntensity"][0]:
            resp["lights"] = "off"
        elif values["LuminousIntensity"] > self.tresholds["LuminousIntensity"][1]:
            resp["lights"] = "on"
        if values["Humidity"] < self.tresholds["Humidity"][0]:
            resp["humidifier"] = "on"
        elif values["Humidity"] > self.tresholds["Humidity"][1]:
            resp["humidifier"] = "off"


        return resp
