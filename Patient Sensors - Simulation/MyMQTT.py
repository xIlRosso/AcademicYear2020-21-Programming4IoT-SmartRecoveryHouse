import paho.mqtt.client as PahoMQTT
import json 

class MyMQTT:
    def __init__(self, clientID, broker, port, notifier=None):
        self.broker = broker
        self.port = port
        self.notifier = notifier
        self.clientID = clientID

        self._topic = ""
        self._isSubscriber = False

        #Create an instane of paho.mqtt.client
        self._paho_mqtt = PahoMQTT.Client(clientID, False)

        #Register the callbacks
        self._paho_mqtt.on_connect = self.myOnConnect
        self._paho_mqtt.on_message = self.myOnMessageReceived

    def myOnConnect(self, paho_mqtt, userdata, flags, rc):
        print ("Connected to %s with result code: %d" % (self.broker, rc))

    def myOnMessageReceived(self, paho_mqtt, userdata, msg):
        #A new message is received
        self.notifier.notify(msg.topic, msg.payload)

    def myPublish(self, topic, msg):
        #If needed, make some computation on the data before publishing
        print("Publishing '%s' with topic '%s'" % (msg, topic))
        #publish to a certain topic with QoS 2
        self._paho_mqtt.publish(topic, json.dumps(msg), 2)

    def mySubscribe(self, topic):
        #If needed, make some computation on the data before subscribing
        print("Subscribing to %s" % (topic))
        #Subscribe to a topic
        self._paho_mqtt.subscribe(topic, 2)

        #Just to remeber that it works also as a subscriber
        self._isSubscriber = True
        self._topic = topic

    def start(self):
        #manage connection to broker
        self._paho_mqtt.connect(self.broker, self.port)
        self._paho_mqtt.loop_start()

    def stop(self):
        if(self._isSubscriber):
            self._paho_mqtt.unsubscribe(self._topic)

        self._paho_mqtt.loop_stop()
        self._paho_mqtt.disconnect()