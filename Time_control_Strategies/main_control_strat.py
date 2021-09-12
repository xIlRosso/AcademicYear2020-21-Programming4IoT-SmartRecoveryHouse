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
from time_shift.time_shift_classes import TimeShift
from actuators_control.actuators_classes import Actuators
from mqtt_methods.mqtt_methods import Publishers, Subscribers    
        

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
        f = requests.get(catalog_address+"controls/values")
        houses = f.json()

        for house in houses:
            #here startup the publisher per house
            myClient = definePaho("myActuatorsClient"+str(i))
            startConnection(myClient, conf["broker"], conf["port"])
            msgToPub = []

            for actuator in house:
                if actuator["name"] == "time":
                    tObj = TimeShift(actuator["tresholds"])
                    actuator["state"] = tObj.run()
                    msgToPub.append(actuator)
                else:
                    if house["houseDevices"]!=[]:
                        for device in house["houseDevices"]:
                            if device["e"][0]["n"] == actuator["name"]:
                                #we need to subscribe for the values of the sensors
                                val = 0
                                #then use the tresholds and check for on/off
                                sObj = Actuators(actuator["tresholds"])
                                actuator["state"] = sObj.run(val)#put the value in run
                                msgToPub.append(actuator)

            myClient.publish(actuator["topic"], payload = json.dumps(msgToPub))
            stopConnection(myClient, actuator["topic"])






    f = requests.get(catalog_address+"/timecontr/sensoract")
    conf2 = f.json()
    print(conf2)

    broker2=conf2['broker']
    port2=conf2['port']
    topics2=conf2['Topics_List']
    sens_tosub=conf2['sensors_to_sub_time_contr']
    tresholds=conf2['treshold_actuators']


    
    A=Actuators(tresholds)
    values={
        "Act1": 0,
        "Act2": 0,
        "Lights": 0,
        "Heating": 0,
        "Humidifier": 0
    }


    t=0
    while t<300:
        # resp=C.time_controlled_actuations()
        p=Publishers()
        # p.run(resp, broker, port, topics)
        time.sleep(1)
        t+=1

        keyz=A.get_keys()
        m=0
        As=[]
        for s in sens_tosub:
            As.append(Subscribers("Actuators"+keyz[m], 
                s,
                broker2,
                port2, 1))
            m+=1
        fg=0
        for actuator in As:
            actuator.start()
            time.sleep(5)
            actuator.stop()
            t+=5

            resp2=A.sensor_based_actuations(fg)

            p.run_act(resp2, broker2, port2, topics2)
            fg+=1

        # values["Act1"]=resp["0"]
        # values["Act2"]=resp["1"]
        values["Heating"]=resp2["heating"]
        values["Humidifier"]=resp2["humidifier"]
        values["Lights"]=resp2["lights"]

        requests.post(catalog_address+"/last_act_status", json=values)



        
        


               

    




    
