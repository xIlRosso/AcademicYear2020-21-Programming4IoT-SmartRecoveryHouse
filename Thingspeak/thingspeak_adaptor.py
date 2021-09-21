from MyMQTT import *
import json, time, os
import urllib.request
import requests
from mqtt_methods.mqtt_methods import *

class mySubscriber():
    def __init__(self, clientID, topic, broker, port, url, key, field):
        self.client = MyMQTT(clientID, broker, port, self)
        self.topic = topic
        self.status = None
        self.threadID = 0
        self.url = url
        self.key = key
        self.field = field

    def start(self):
        self.client.start()
        self.client.mySubscribe(self.topic)

    def stop(self):
        self.client.stop()
    
    def notify(self, topic, payload):
        payload = json.loads(payload)
        if payload != []:
            # for sensor in payload:
            sensor = payload
            new_status = sensor["e"][0]["v"]
            name_sensor = sensor["e"][0]["n"]
            self.status = new_status
            pubID = sensor["bn"]
            timestamp = sensor["e"][0]["t"]
            print(f"The measured value is {new_status} at {timestamp} by {pubID}")

    # push data to thingspeak 
            self.thingspeak_post(new_status, name_sensor)
                # time.sleep(20)

    ############## pushing to thingspeak ####################""

    def thingspeak_post(self, val, name_sensor):
        field = self.field[name_sensor]
        URL = self.url
        KEY = self.key
        HEADER = '&field{}={}'.format(field, val)
        NEW_URL = URL+KEY+HEADER
        print(NEW_URL)
        data=urllib.request.urlopen(NEW_URL)

    
class Catalog(mySubscriber):

    def __init__(self, catalog_address, url, key, field):
        self.url = url
        self.key = key
        self.field = field

# "https://api.thingspeak.com/channels/1356837/feeds.json"
# 
    

def clear_thingspeak(clear_url):
    requests.delete(clear_url)



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


    #we need url, key thingspeak, broker, port, field, clearURL

    r = requests.get(catalog_address+"/thingspeak/settings")

    conf = r.json()
    broker = conf["broker"]
    port = conf["port"]

    #send catalog address to thingspeak

    clear_thingspeak(conf["clearURL"])
    cObj = Catalog(catalog_address, conf["url"], conf["key"], conf["field"])    
    cObj.thingspeak_post(catalog_address, "address")

    """
    field = {
        "temperature" : 1,
        "weight" : 2,
        "heartrate" : 3,
        "address" : 4
    }
    """

    #we need from the catalog which patient to highlight in thingspeak
    oldID = ""
    while True:

        #here get the unique id key: uniqueID
        
        r = requests.get(catalog_address+"/thingspeak/highlightedPatient")
        unID = r.json()
        

        if unID != oldID: 
            clear_thingspeak(conf["clearURL"])
            cObj.thingspeak_post(catalog_address, "address")

            
        #here get the topic key: topicsNeeded

        r = requests.get(catalog_address+"/thingspeak/highlighted/"+unID)
        topic_sens_t = r.json()

        #here get the topic to subscribe to the highlighted patient

        mySub = mySubscriber("AlexSubs920318_client1", topic_sens_t, broker, port,  conf["url"], conf["key"], conf["field"])

        mySub.start()
        time.sleep(60)
        mySub.stop()
        oldID = unID
