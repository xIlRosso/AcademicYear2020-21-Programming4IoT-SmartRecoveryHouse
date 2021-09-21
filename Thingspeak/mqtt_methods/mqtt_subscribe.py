import paho.mqtt.client as PahoMQTT
import json
import urllib.request

class SubscriberTh:


    def __init__(self, clientID, topic, broker, port, url, key, field):
        self.clientID=clientID
        self._paho_client=PahoMQTT.Client(self.clientID, True)
        self.topic=topic
        self.messageBroker=broker
        self._paho_client.on_connect=self.myOnConnect
  
        self._paho_client.on_message=self.myOnMsgReceived
       
        self.port=port

        self.url = url
        self.key = key
        self.field = field
        
    def start(self):
        self._paho_client.connect(self.messageBroker)
        self._paho_client.loop_start()
        self._paho_client.subscribe(self.topic, 2)
        
    def stop(self):
        self._paho_client.unsubscribe(self.topic)
        self._paho_client.loop_stop()
        self._paho_client.disconnect()
        
    def myOnConnect(self, paho_mqtt, userdata, flags, rc):
        print("Connection successful to "+self.messageBroker+" with result code: "+str(rc))
        
    def myOnMsgReceived(self, paho_mqtt, userdata, msg):
        payload = json.loads(msg.payload)
        print("Received something!")
        print(json.dumps(payload))
        if payload != {}:
            print("entered the if payload != {")
            for sensor in payload:
                print("entered the for sensor in payload")
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
        print("thingspeak_post is called!")
        field = self.field[name_sensor]
        URL = self.url
        KEY = self.key
        HEADER = '&field{}={}'.format(field, val)
        NEW_URL = URL+KEY+HEADER
        print(NEW_URL)
        data=urllib.request.urlopen(NEW_URL)
        
    
            
