from MyMQTT import *
from Curves import *
import numpy as np
import json, time, os

class myPublisher_temp():
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

        if(os.path.isfile("temp_log1.json")):
            json_log = json.load(open("temp_log1.json", "r"))
        else:
            json_log = {"bn" : message["bn"],"e" : []}

        json_log["e"].append(message["e"])                        
        #json_log[payload["bn"]].append(payload["e"])
        json.dump(json_log, open("temp_log1.json", "w"),indent=4)
    
if __name__ == "__main__":
    conf = json.load(open("settings.json"))
    broker = conf["broker"]
    port = conf["port"]
    msg = conf["devicesList"][0]
    topic = conf["devicesList"][0]["bn"]

    print("What case do you want to apply?")
    print("r - Normal [36.5 ; 37.5]")
    print("l - Low Temp [< 35]")
    print("h - High Temp [> 40]\n")

    cmd = input()

    sim = Simulation(36.5,37.5)

    if cmd == "r":
        c=input("Want to implement fever scenario?(y:Yes/n:No)\n")
        sim.Norm_Temp(c)
    elif cmd == "l":
        sim.Low_Temp()    
    elif cmd == "h":
        sim.High_Temp()

    myPubl = myPublisher_temp("SRH_SensTemp", topic, broker, port, msg)    
    myPubl.start()
    
    for i in sim.sf:
        myPubl.publish(i)
        time.sleep(60)
    myPubl.stop()






