# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 15:54:29 2021

@author: ilros
"""
import paho.mqtt.client as PahoMQTT
import json
import time

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
   
    
    def run(self,pub, broker, port, topics, iterations):
        for i in range(0, iterations):
            myClient=self.definePaho('ClientTest'+str(i))
            self.startConnection(myClient, broker, port)
            self.publishMessage(myClient, topics, json.dumps(pub))
            
            self.stopConnection(myClient, topics)
            time.sleep(1)
            
        