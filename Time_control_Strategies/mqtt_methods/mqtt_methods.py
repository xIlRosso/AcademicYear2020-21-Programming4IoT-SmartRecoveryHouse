# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 15:54:29 2021

@author: ilros
"""
import paho.mqtt.client as PahoMQTT
import json


class Publishers():

    def definePaho(self, clientID):
        return  PahoMQTT.Client(clientID)
    
    def startConnection (self, myClient, broker, port):
        myClient.connect(host=broker, port=port)
        myClient.loop_start()
    
    
    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload)) 
    
    def stopConnection (self,myClient, topic):
        myClient.loop_stop()
        myClient.disconnect()
     
    def publishMessage (self,myClient, topic, msg):
        print("Publishing "+msg+" on topic "+topic)
        myClient.publish(topic, msg)
    
    def subscribeClient (self,myClient, topic):
        myClient.subscribe(topic)
   
    
    def run(self,pub, broker, port, topics):
        for i in range(0, len(topics)):
            myClient=self.definePaho('ClientTest'+str(i))
            self.startConnection(myClient, broker, port)
            self.publishMessage(myClient, topics[i], json.dumps(pub[str(i)]))
            self.stopConnection(myClient, topics[i])

    def run_act(self, pub, broker, port, topics):
        i=0
        for topic in topics:
            myClient=self.definePaho('ClientAct'+str(i))
            self.startConnection(myClient, broker, port)
            if i == 0:
                self.publishMessage(myClient, topic, json.dumps(pub["lights"]))
            elif i == 1:
                self.publishMessage(myClient, topic, json.dumps(pub["heating"]))
            elif i == 2:
                self.publishMessage(myClient, topic, json.dumps(pub["humidifier"]))
            self.stopConnection(myClient, topic)
            i+=1


class Subscribers:


    def __init__(self, clientID, topic, broker, port, actuators):
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
        json.dump(data, open('Time_control_strategies/catalog_url.json','w'))
        print(json.dumps(data))
        
