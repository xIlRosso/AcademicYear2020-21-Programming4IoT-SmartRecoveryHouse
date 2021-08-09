from MyMQTT import *
from Curves import *
import json, random, time, os

class myPublisher_HR():
    def __init__(self, clientID, topic, broker, port, msg):
        self.client = MyMQTT(clientID, broker, port, self)
        self.topic = topic
        self.status = None
        self.__message = msg

    def start(self):
        self.client.start()

    def stop(self):
        self.client.stop()

    def publish(self, value1, value2):
        message = self.__message
        message["e"][0]["v"] = value1
        message["e"][0]["t"] = str(time.time())
        message["e"][1]["v"] = value2
        message["e"][1]["t"] = str(time.time())        
        self.client.myPublish(self.topic, message)

        if(os.path.isfile("HrOs_log1.json")):
            json_log = json.load(open("HrOs_log1.json", "r"))
        else:
            json_log = {"bn" : message["bn"],"e" : []}

        json_log["e"].append(message["e"])
        json.dump(json_log, open("HrOs_log1.json", "w"),indent=4)
    
if __name__ == "__main__":
    conf = json.load(open("settings.json"))
    broker = conf["broker"]
    port = conf["port"]
    msg = conf["devicesList"][1]
    topic = conf["devicesList"][1]["bn"]
    
    print("What case do you want to apply?")
    print("r - Rest [60 ; 75]")
    print("l - Low Heart Rete [55 ; 75]")
    print("h - High Heart Rate [60 ; 100]\n")
    cmd = input()

    sim = Simulation(60,75)

    if cmd == "r":
        sim.Rest_HR()
    elif cmd == "l":
        c=input("Want to implement heart attack scenario?(y:Yes/n:No)\n")
        sim.Low_HR(c)    
    elif cmd == "h":
        c=input("Want to implement heart attack scenario?(y:Yes/n:No)\n")
        sim.High_HR(c)

    x = sim.sf

    print("What case do you want to apply?")
    print("r - Normal [95 ; 100]")
    print("l - Low Oxygen [< 95]")
    print("h - Extreme Low Oxygen [< 85]\n")
    cmd = input()

    sim = Simulation(95,100)

    if cmd == "r":
        sim.Norm_OS()
    elif cmd == "l":
        sim.Low_OS()    
    elif cmd == "h":
        sim.Dang_OS()

    y = sim.sf

    myPubl = myPublisher_HR("SRH_SensHR_OS", topic, broker, port, msg)    
    myPubl.start()

    count = 0
    for i in x:
        myPubl.publish(i,y[count])
        count+=1
        print(count)
        time.sleep(60)
    myPubl.stop()