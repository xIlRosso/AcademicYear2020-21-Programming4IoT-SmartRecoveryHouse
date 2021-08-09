from MyMQTT import *
import json, time, os

class mySubscriber():
    def __init__(self, clientID, topic, broker, port):
        self.client = MyMQTT(clientID, broker, port, self)
        self.topic = topic
        self.status = None

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
        print(f"The led has been set to {new_status} at {timestamp} by {pubID}")

        if(os.path.isfile("temp_log.json")):
            json_log = json.load(open("temp_log.json", "r"))
        else:
            json_log = {"bn" : payload["bn"],"e" : []}

        json_log["e"].append(payload["e"][0])                        
        #json_log[payload["bn"]].append(payload["e"])
        json.dump(json_log, open("temp_log.json", "w"),indent=2)

if __name__ == "__main__":
    conf = json.load(open("settings.json"))
    broker = conf["broker"]
    port = conf["port"]
    topic = conf["devicesList"][0]["bn"]
    mySub = mySubscriber("AlexSubs920318", topic, broker, port)

    mySub.start()
    
    while(1):
        time.sleep(1)
    mySub.stop()