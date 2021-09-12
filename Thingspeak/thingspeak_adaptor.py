from MyMQTT import *
import json, time, os
import threading
import urllib.request
import requests
from mqtt_methods.mqtt_methods import *

class mySubscriber():
    def __init__(self, clientID, topic, broker, port, threadID):
        self.client = MyMQTT(clientID, broker, port, self)
        self.topic = topic
        self.status = None
        self.threadID = threadID

    def start(self):
        self.client.start()
        self.client.mySubscribe(self.topic)

    def stop(self):
        self.client.stop()
    
    def notify(self, topic, payload):
        payload = json.loads(payload)
        new_status = payload["e"][0]["v"]
        self.status = new_status
        pubID = payload["bn"]
        timestamp = payload["e"][0]["t"]
        print(f"The measured value is {new_status} at {timestamp} by {pubID}")

        # write data to json file
        '''if(os.path.isfile("temp_log.json")):
            json_log = json.load(open("temp_log.json", "r"))
        else:
            json_log = {"bn" : payload["bn"],"e" : []}

        json_log["e"].append(payload["e"][0])          
        json.dump(json_log, open("temp_log.json", "w"),indent=2)'''

        # push data to thingspeak 
        self.thingspeak_post(new_status, self.threadID)

    ############## pushing to thingspeak ####################""

    def thingspeak_post(self, val, threadID):
        field = threadID + 1
        URL = 'https://api.thingspeak.com/update?api_key='
        KEY = 'N673MD9IWBGMB7N2'
        HEADER = '&field{}={}'.format(field, val)
        NEW_URL = URL+KEY+HEADER
        print(NEW_URL)
        data=urllib.request.urlopen(NEW_URL)
    
def catalog_addr_post(val):
    field = 4
    URL = 'https://api.thingspeak.com/update?api_key='
    KEY = 'N673MD9IWBGMB7N2'
    HEADER = '&field{}={}'.format(field, val)
    NEW_URL = URL+KEY+HEADER
    print(NEW_URL)
    data=urllib.request.urlopen(NEW_URL)


if __name__ == "__main__":
    with open("Thingspeak/catalog_mqtt_settings.json","r") as json_in:
        setsCatalog = json.load(json_in)

    S=Subscribers(setsCatalog["ID"], setsCatalog["topic"], setsCatalog["broker"], setsCatalog["port"])
    i=0
    while i<10:
        S.start()
        time.sleep(4)
        S.stop()
        i+=2
    i=0
    

    with open("Thingspeak/catalog_url.json") as json_in:
        dat=json.load(json_in)
        catalog_address=dat["url_catalog"]

    r = requests.get(catalog_address+"/thingspeak/settings")

    conf = r.json()
    broker = conf["broker"]
    port = conf["port"]

    #send catalog address to thingspeak

    catalog_addr_post(catalog_address)    

    # temperature
    topic_temp = conf["Topics_List"][0]
    mySub_temp = mySubscriber("AlexSubs920318_client1", topic_temp, broker, port, 0)

    # heart rate
    topic_hr = conf["Topics_List"][1]
    mySub_hr = mySubscriber("AlexSubs920318_client2", topic_hr, broker, port, 1)


    # weight
    topic_weight = conf["Topics_List"][2]
    mySub_weight = mySubscriber("AlexSubs920318_client3", topic_weight, broker, port, 2)

    mySub_temp.start()
    mySub_hr.start()
    mySub_weight.start()
    
    while (1):
        time.sleep(10)
        
    mySub_temp.stop()
    mySub_hr.stop()
    mySub_weight.stop()
    
