import json
import  time
import numpy as np
import paho.mqtt.client as PahoMQTT
import requests
import random
from mqtt_methods.mqtt_methods import Subscribers, Publishers


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

def generate_value(meanV, varV) -> float:
    N=1000
    x1=np.random.normal(meanV,varV,N)
    no=random.randint(0,len(x1)-1)
    
    return x1[no]




if __name__ == "__main__":

    with open("House Sensors/catalog_mqtt_settings.json","r") as json_in:
            setsCatalog = json.load(json_in)

    S=Subscribers(setsCatalog["ID"], setsCatalog["topic"], setsCatalog["broker"], setsCatalog["port"])

    i=0
    while i<10:
        S.start()
        time.sleep(4)
        S.stop()
        i+=2

    with open("House Sensors/catalog_url.json") as json_in:
        dat=json.load(json_in)
        catalog_address=dat["url_catalog"]

    #ok so first of all get configuration file
    #in the config should be mean and var for every type of sensor
    #broker, port

    r = requests.get(catalog_address+"/sensors/house")

    conf = r.json()

    #now set up the loop for the list of devices

    

    i=0

    while i<1000:
        f = requests.get(catalog_address+"/sensors/house_list") # get the list of houses
        houses = f.json()

        for house in houses:
            myClient = definePaho("myHouseClient"+str(i))
            startConnection (myClient, conf["broker"], conf["port"])
            msgToPub=[]
            for sensor in house:
                sensor["e"][0]["v"]= generate_value(conf[sensor["e"][0]["n"]]["mean"], conf[sensor["e"][0]["n"]]["var"])
                sensor["e"][0]["t"] = time.asctime()
                requests.post(catalog_address + "/updateSens/house/"+sensor["patientID"], json = sensor)
                msgToPub.append(sensor)

            myClient.publish(sensor["topic"], payload = json.dumps(msgToPub))
            stopConnection(myClient, sensor["topic"])
            print(json.dumps(msgToPub))
            print("Computing and publishing the next house")


        time.sleep(4)


