import json
import requests
import time
import numpy as np
import paho.mqtt.client as PahoMQTT


class Subscribers:


    def __init__(self, clientID, topic, broker, port):
        self.clientID=clientID
        self._paho_client=PahoMQTT.Client(self.clientID, True)
        self.topic=topic
        self.messageBroker=broker
        self._paho_client.on_connect=self.myOnConnect
        
        self._paho_client.on_message=self.myOnMsgReceived
        
        self.port=port
        
    def start(self):
        self._paho_client.connect(self.messageBroker)
        self._paho_client.loop_start()
        self._paho_client.subscribe(self.topic, qos = 2)
        
    def stop(self):
        self._paho_client.unsubscribe(self.topic)
        self._paho_client.loop_stop()
        self._paho_client.disconnect()
        
    def myOnConnect(self, paho_mqtt, userdata, flags, rc):
        print("Connection successful to "+self.messageBroker+" with result code: "+str(rc))
        
    def myOnMsgReceived(self, paho_mqtt, userdata, msg):
        data=json.loads(msg.payload)
        json.dump(data, open('Time_control_strategies/sens_act.json','w'))
        print(json.dumps(data))



class Actuators:
    def __init__(self, data = 0):
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

        if val > treshHigh:
            state = "off"
        elif val >= treshLow and val <= treshHigh:
            state = "on"
        elif val < treshLow:
            state = "on"

        return state

    def run_sub(self, topic, broker, port) -> None:
        c = Subscribers("ClientSomething"+topic, topic, broker, port)
        c.start()
        time.sleep(4)
        c.stop()

