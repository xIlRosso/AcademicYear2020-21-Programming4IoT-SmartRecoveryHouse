# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 15:54:29 2021

@author: ilros
"""
import paho.mqtt.client as PahoMQTT
import json



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
        self._paho_client.subscribe(self.topic, 2)
        
    def stop(self):
        self._paho_client.unsubscribe(self.topic)
        self._paho_client.loop_stop()
        self._paho_client.disconnect()
        
    def myOnConnect(self, paho_mqtt, userdata, flags, rc):
        print("Connection successful to "+self.messageBroker+" with result code: "+str(rc))
        
    def myOnMsgReceived(self, paho_mqtt, userdata, msg):
        d=json.loads(msg.payload)
        data={
            "url_catalog" : d
        }
        json.dump(data, open('Telegram/catalog_url.json','w'))
        print(json.dumps(data))
        
    
            
