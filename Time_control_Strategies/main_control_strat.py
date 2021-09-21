# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 15:18:44 2021

@author: ilros
"""

import json
import requests
import time
import numpy as np
import paho.mqtt.client as PahoMQTT
import os.path
from time_shift.time_shift_classes import TimeShift
from actuators_control.actuators_classes import Actuators
from mqtt_methods.mqtt_methods import Subscribers    
        

def definePaho(clientID):
    return  PahoMQTT.Client(clientID)

def startConnection (myClient, broker, port):
    myClient.connect(host=broker, port=port, keepalive=60, bind_address="")


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload)) 

def stopConnection (myClient, topic):
    myClient.loop_stop()
    myClient.disconnect()
 
def publishMessage (myClient, topic, msg):
    myClient.publish(topic, msg)

def subscribeClient (myClient, topic):
    myClient.subscribe(topic)



if __name__=='__main__':

    with open("Time_Control_Strategies/catalog_mqtt_settings.json","r") as json_in:
        setsCatalog = json.load(json_in)

    S=Subscribers(setsCatalog["ID"], setsCatalog["topic"], setsCatalog["broker"], setsCatalog["port"])
    i=0
    while i<10:
        S.start()
        time.sleep(4)
        S.stop()
        i+=2

    with open("Time_control_strategies/catalog_url.json") as json_in:
        dat=json.load(json_in)
        catalog_address=dat["url_catalog"]

# a comment

    #here i need the list of actuators, the list of topics for sensor subscription
    #for the settings i need topic, broker and that's it


    r=requests.get(catalog_address+"/controls/settings")
    conf=r.json()
    print(conf)


    broker=conf['broker']
    port=conf['port']


    #set up the checking loop:

    i=0
    while i<1000:
        #get actuators and topic info values
        f = requests.get(catalog_address+"/controls/house_list")
        houses = f.json()
        
        houses = houses["houses"]

        for house in houses:
            #here startup the publisher per house
            myClient = definePaho("myActuatorsClient"+str(i))
            startConnection(myClient, conf["broker"], conf["port"])
            msgToPub = []

            for actuator in house["actList"]:
                if actuator["name"] == "time":
                    tObj = TimeShift(actuator["tresholds"])
                    actuator["state"] = tObj.run()
                    requests.post(catalog_address+"/updateSens/actuator/"+actuator["patientID"], json = actuator)
                    msgToPub.append(actuator)
                else:
                    if house["houseDevices"]!=[]:
                        for device in house["houseDevices"]:
                            if device["e"][0]["n"] == actuator["name"]:
                                #we need to subscribe for the values of the sensors
                                s2Obj = Actuators()
                                s2Obj.run_sub(device["topic"], conf["broker"], conf["port"])
                                
                                if os.path.isfile("Time_Control_strategies/sens_act.json"):
                                    with open("Time_Control_strategies/sens_act.json") as json_in:
                                        val_tmp = json.load(json_in)
                                    for sensor in val_tmp:
                                        if sensor["e"][0]["n"]==actuator["name"]:
                                            val = sensor["e"][0]["v"]

                                    #then use the tresholds and check for on/off
                                    sObj = Actuators(actuator["tresholds"])
                                    actuator["state"] = sObj.run(val)#put the value in run
                                    requests.post(catalog_address+"/updateSens/actuator/"+actuator["patientID"], json = actuator)
                                    msgToPub.append(actuator)

            myClient.publish(actuator["topic"], payload = json.dumps(msgToPub))
            print(json.dumps(msgToPub))
            stopConnection(myClient, actuator["topic"])
            msgToPub.clear()

               

    




    
