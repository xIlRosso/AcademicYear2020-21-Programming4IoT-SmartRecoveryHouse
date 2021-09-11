import json
import  time
import numpy as np
import paho.mqtt.client as PahoMQTT
import requests
import random
from mqtt_methods.mqtt_methods import Subscribers, Publishers



def myComment (temp, luminousIntensity, humidity):
    msg = ""
    if temp > 25:
        msg = msg + "Warning! temp is high, "
    if temp < 19:
        msg = msg +  "Warning! temp is low, "
    
    if luminousIntensity > 600:
        msg = msg +  "light is high, "
    if luminousIntensity < 400:
        msg = msg +  "light is low, "
        
    if humidity > 50:
        msg = msg +  "humidity is high, "
    if humidity < 30:
        msg = msg +  "humidity is low, " 
    
    if msg == "":
        return "all parameters are ok"
    else:
        return msg


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

    with open("House Sensors/catalog_url.json") as json_in:
        dat=json.load(json_in)
        catalog_address=dat["url_catalog"]

    i=0
    while i<10:
        S.start()
        time.sleep(4)
        S.stop()
        i+=2

    #ok so first of all get configuration file
    #in the config should be mean and var for every type of sensor
    #broker, port

    r = requests.get(catalog_address+"/sensors/house")

    conf = r.json()

    #now set up the loop for the list of devices

    

    i=0

    while i<1000:
        r = requests.get(catalog_address+"/sensors/house_list") # get the list of houses
        houses = r.json()

        for house in houses:
            myClient = definePaho("myTestClient"+str(i))
            startConnection (myClient, conf["broker"], conf["port"])
            msgToPub=[]
            for sensor in house:
                sensor["e"][0]["v"]= generate_value(conf[sensor["e"][0]["n"]]["mean"], conf[sensor["e"][0]["n"]]["var"])
                sensor["e"][0]["t"] = time.asctime()
                msgToPub.append(sensor)

            myClient.publish(sensor["topic"], payload = json.dumps(msgToPub))
            stopConnection(myClient, sensor["topic"])

            print("Computing and publishing the next house")


        time.sleep(1)





    # # conf = json.load(open("settings.json"))
    # r = requests.get(catalog_address+"/sensor/housedev")
    # conf = r.json()
    # myValues = conf
    # broker = conf["broker"]
    # port = conf["port"]
    # msg = conf["devicesList"][0]
    # topics = conf["Topics_List"]

    # myClient = definePaho("myTestClinet")

    # startConnection (myClient, broker, port)

    # print("Start Connection")

    # senml_format={
    #     "devicesList" : [
    #         {
    #             "bn" : "",
    #             "e" : [
    #                 {
    #                     "n" : "",
    #                     "u" : "",
    #                     "t" : 0,
    #                     "v" : 0
    #                 }
    #             ]
    #         }
    #     ]
    # }


    # values = {
    #         "Temperature" : 0,
    #         "LuminousIntensity" : 0,
    #         "Humidity" : 0
    #     }   

    # for j in range(200):  
        
    #     result = {}
    #     sensorUnits = {}

    #     sensorNum = len(conf["devicesList"])
        

    #     for i in range(0,sensorNum):
    #         resp=senml_format.copy()
    #         topic = topics[i]
    #         normalSensorValue = conf["devicesList"][i]["e"][0]["v"]
    #         varianceSensorValue = conf["devicesList"][i]["e"][0]["std"]
    #         resp["devicesList"][0]["e"][0]["v"] = np.random.normal(normalSensorValue,varianceSensorValue)
    #         #conf["devicesList"][i]["e"][0]["v"] = normalSensorValue
    #         resp["devicesList"][0]["e"][0]["u"] = conf["devicesList"][i]["e"][0]["u"]
    #         resp["devicesList"][0]["e"][0]["n"] =  conf["devicesList"][i]["e"][0]["n"]
    #         resp["devicesList"][0]["e"][0]["t"] = time.time()
    
            
    #         myClient.publish(topic, payload = json.dumps(resp))
    #         print("Publishing: "+json.dumps(resp))
    #         time.sleep(1)
    #         values[resp["devicesList"][0]["e"][0]["n"]] = resp["devicesList"][0]["e"][0]["v"]
        

        
    #     requests.post(catalog_address+"/last_house_meas", json=values)


        
    #     # myPayLoad = ""
    #     # for k in result:
    #     #     myPayLoad = myPayLoad + k + "= " + str(result[k]) + " " + str(sensorUnits[k]) + " and "
        
    #     # myPayLoad = myPayLoad[:len(myPayLoad) - 5]
    #     # myPayLoad = myPayLoad + ". So: " + myComment(result["Temperature"], result["LuminousIntensity"], result["Humidity"])

    #     # print(myPayLoad)
        
    #     # myClient.publish(topic, payload = myPayLoad , qos=2, retain= True)


    #     # outPutJsonName = 'myValuesJson_' + str(j+1) + '.json'
        
    #     # # with open(outPutJsonName, 'w') as outfile:
    #     # #     json.dump(myValues, outfile)
                        
    # stopConnection(myClient, topic)

    # print("Close Connection")





