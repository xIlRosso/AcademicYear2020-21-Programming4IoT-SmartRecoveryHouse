#programming_for_iot/aa2021/SmartRecoveryHouse/thatdomaincom/body/temperature


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
        print(json.dumps(data))



if __name__ == "__main__":

    sd = Subscribers("ClientSomething12345", "programming_for_iot/aa2021/SmartRecoveryHouse/thatdomaincom/body", "broker.hivemq.com", 1883)

    sd.start()
    i=0
    while i<50:
        time.sleep(5)
        i+=5

    sd.stop()