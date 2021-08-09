from MyMQTT import *
from Curves import *
import numpy as np
import json, time, os

class myPublisher_weight():
    def __init__(self, clientID, topic, broker, port, msg):
        self.client = MyMQTT(clientID, broker, port, self)
        self.topic = topic
        self.status = None
        self.__message = msg

    def start(self):
        self.client.start()

    def stop(self):
        self.client.stop()

    def publish(self, value):
        message = self.__message
        message["e"][0]["v"] = value
        message["e"][0]["t"] = str(time.time())
        self.client.myPublish(self.topic, message)

        if(os.path.isfile("weight_log1.json")):
            json_log = json.load(open("weight_log1.json", "r"))
        else:
            json_log = {"bn" : message["bn"],"e" : []}

        json_log["e"].append(message["e"])                        
        #json_log[payload["bn"]].append(payload["e"])
        json.dump(json_log, open("weight_log1.json", "w"),indent=4)

if __name__ == "__main__":
    conf = json.load(open("settings.json"))
    broker = conf["broker"]
    port = conf["port"]
    msg = conf["devicesList"][2]
    topic = conf["devicesList"][2]["bn"]
    
    print("What case do you want to apply?")
    print("r - Normal [62 ; 62.5]")
    print("l - Low Weight [< 62]")
    print("h - High Weight [> 62.5]\n")

    cmd = input()

    sim = Simulation(36.5,37.5)

    if cmd == "r":
        sim.Norm_Weig()
    elif cmd == "l":
        sim.Low_Weig()    
    elif cmd == "h":
        sim.High_Weig()

    myPubl = myPublisher_weight("SRH_SensWeight", topic, broker, port, msg)    
    myPubl.start()
    
    for i in sim.sf:
        myPubl.publish(i)
        time.sleep(60)
    myPubl.stop()


