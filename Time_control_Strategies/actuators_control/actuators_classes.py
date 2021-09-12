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


    def run(self, val) -> str:
        treshLow = self.tresholds[0]
        treshHigh = self.tresholds[1]
        state = ""

        if val < treshHigh:
            state = "off"
        elif val >= treshLow:
            state = "on"

        return state



    def sensor_based_actuations(self, idn):
        pass