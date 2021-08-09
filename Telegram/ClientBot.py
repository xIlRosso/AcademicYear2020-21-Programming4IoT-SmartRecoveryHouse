import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import json, time
import requests
from MyMQTT import *
from mqtt_methods.mqtt_methods import Subscribers


flagID=999
class MyBot:
    def __init__(self,token):
        # Local Token
        self.tokenBot = token
        # Catalog Token
        # self.tokenBot = requests.get("http://catalogIP/telegram_token").json()["telegramToken"]
        self.bot = telepot.Bot(self.tokenBot)
        MessageLoop(self.bot,{'chat' : self.on_chat_message}).run_as_thread()


    def on_chat_message(self,msg):
        content_type, chat_type, chat_ID = telepot.glance(msg)
        message = msg['text']

        self.bot.sendMessage(chat_ID,text="you sent:\n"+ message)

class SwitchBot:
    def __init__(self, token, broker, port, topic, address):
        self.catalog = address
        self.tokenBot = token
        self.bot = telepot.Bot(self.tokenBot)
        self.client = MyMQTT("telegramBot",broker,port,None)
        self.client.start()
        self.topic = topic
        self._message = {'bn': "telegrambot",
                         'e':
                         [
                            {'n': 'switch', 'v': '', 't': '', 'u': 'bool'}, 
                         ]
                        }
        MessageLoop(self.bot, {'chat': self.on_chat_message,
                                'callback_query': self.on_callback_query}).run_as_thread()

    def measurements(self,sensor_name,sens_type):
        
        if sens_type == 1:
            r = requests.get(catalog_address+"/telegram_bot/sens_measurements")
            values = r.json()
        elif sens_type == 2:
            r = requests.get(catalog_address+"/telegram_bot/house_measurements")
            values = r.json()        
        elif sens_type == 3:
            r = requests.get(catalog_address+"/telegram_bot/actuators_status")
            values = r.json() 
        elif sens_type == 4:
            r = requests.get(catalog_address+"/telegram_bot/regression_status")
            values = r.json()
        return values[sensor_name]
    


    def on_chat_message(self, msg):
        content_type, chat_type, chat_ID = telepot.glance(msg)
        message = msg['text']
        global flagID
        r = requests.get(catalog_address+"/telegram_bot/pin_ids")
        pins = r.json()
        f = requests.get(catalog_address+"/telegram_bot/patient_alarms")
        alarm = f.json()

        if message == "/start":
            buttons=[[InlineKeyboardButton(text=f'Doctor', callback_data=f'Doctor'),
                    InlineKeyboardButton(text=f'Caregiver', callback_data=f'Caregiver'),
                    InlineKeyboardButton(text=f'Patient', callback_data=f'Patient')]]
            keyboard= InlineKeyboardMarkup(inline_keyboard=buttons)
            self.bot.sendMessage(chat_ID, text='Please identify yourself', reply_markup=keyboard)
            
        elif message == "/sens":
            buttons=[[InlineKeyboardButton(text=f'Temperature', callback_data=f'Temperature measurement {self.measurements("Temp",1)}'),
                    InlineKeyboardButton(text=f'HeartBeat', callback_data=f'Heart Beat measurement {self.measurements("HeartR",1)}'),
                    InlineKeyboardButton(text=f'Weight', callback_data=f'Weight measurement {self.measurements("Weight",1)}')]]
            keyboard= InlineKeyboardMarkup(inline_keyboard=buttons)

            self.bot.sendMessage(chat_ID, text='Select a patient sensor', reply_markup=keyboard)

        elif message == "/house":
            buttons=[[InlineKeyboardButton(text=f'Temperature', callback_data=f'Temperature measurement {self.measurements("Temperature",2)}'),
                    InlineKeyboardButton(text=f'LightIntensity', callback_data=f'LightIntensity measurement {self.measurements("LuminousIntensity",2)}'),
                    InlineKeyboardButton(text=f'Humidity', callback_data=f'Humidity measurement {self.measurements("Humidity",2)}')]]
            keyboard= InlineKeyboardMarkup(inline_keyboard=buttons)
            self.bot.sendMessage(chat_ID, text='Select a house sensor', reply_markup=keyboard)

        elif message == "/actuat" and (flagID == 1 or flagID == 2):
            buttons=[[InlineKeyboardButton(text=f'Act 1', callback_data=f'State Actuator 1 {self.measurements("Actuator1",3)}'),
                    InlineKeyboardButton(text=f'Act 2', callback_data=f'State Actuator 2 {self.measurements("Actuator2",3)}'),
                    InlineKeyboardButton(text=f'Lights', callback_data=f'State Lights {self.measurements("Lights",3)}'),
                    InlineKeyboardButton(text=f'Heating', callback_data=f'State Heating {self.measurements("Heating",3)}'),
                    InlineKeyboardButton(text=f'Humidifier', callback_data=f'State Humidifier {self.measurements("Humidifier",3)}')]]
            keyboard= InlineKeyboardMarkup(inline_keyboard=buttons)
            self.bot.sendMessage(chat_ID, text='Select an actuator', reply_markup=keyboard)

        elif message == "/regres" and flagID == 1:
            buttons=[[InlineKeyboardButton(text=f'Temperature', callback_data=f'Temperature regression {self.measurements("Temp",4)}'),
                    InlineKeyboardButton(text=f'HeartBeat', callback_data=f'Heart Beat regression {self.measurements("HeartR",4)}'),
                    InlineKeyboardButton(text=f'Weight', callback_data=f'Weight regression {self.measurements("Weight",4)}')]]
            keyboard= InlineKeyboardMarkup(inline_keyboard=buttons)
            self.bot.sendMessage(chat_ID, text='Select a sensor for the regression', reply_markup=keyboard)

        elif message == pins["Doctor_PIN"]:
            flagID = 1
            self.bot.sendMessage(chat_ID, text='Access to /sens, /regres, /actuat, /house commands is granted')

        elif message == pins["Caregiver_PIN"]:
            flagID = 2
            self.bot.sendMessage(chat_ID, text='Access to /sens, /actuat, /house command is granted')

        elif message == pins["Patient_PIN"]:
            flagID = 3
            self.bot.sendMessage(chat_ID, text='Access to /sens, /house commands is granted')

        else:
            self.bot.sendMessage(chat_ID, text="Command not supported")
        
        if alarm["Temp"] == 1:
            self.bot.sendMessage(chat_ID, text="Warning! Patient Temperature is High")
        elif alarm["Temp"] == 2:
            self.bot.sendMessage(chat_ID, text="Warning! Patient Temperature is Low")   

        if alarm["Weight"] == 1:
            self.bot.sendMessage(chat_ID, text="Warning! Patient Weight is High")
        elif alarm["Weight"] == 2:
            self.bot.sendMessage(chat_ID, text="Warning! Patient Weight is Low") 

        if alarm["HeartR"] == 1:
            self.bot.sendMessage(chat_ID, text="Warning! Patient HeartRate is High")
        elif alarm["HeartR"] == 2:
            self.bot.sendMessage(chat_ID, text="Warning! Patient HeartRate is Low") 

    def on_callback_query(self,msg):
        query_ID, chat_ID, query_data = telepot.glance(msg,flavor='callback_query')  
        payload = self._message.copy() 
        payload['e'][0]['v'] = query_data
        payload['e'][0]['t'] = time.time()
        self.client.myPublish(self.topic, payload)
        
        message = msg['message']['text']
        print (message)
        if message == "Please identify yourself":
            self.bot.sendMessage(chat_ID, text=f"Welcome {query_data}, insert the pin")
        elif message == "Select a patient sensor":
            self.bot.sendMessage(chat_ID, text=f"{query_data}")
        elif message == "Select a house sensor":
            self.bot.sendMessage(chat_ID, text=f"{query_data}")
        elif message == "Select an actuator":
            self.bot.sendMessage(chat_ID, text=f"{query_data}") 
        elif message == "Select a sensor for the regression":
            self.bot.sendMessage(chat_ID, text=f"{query_data}")                

if __name__ == "__main__":

    S=Subscribers("Beacon_Capture1234", 
    "programming_for_iot/aa2021/SmartRecoveryHouse/catalog_public_address",
    "broker.hivemq.com",
    1883, 0
    )
    i=0
    while i<10:
        S.start()
        time.sleep(4)
        S.stop()
        i+=2

    with open("Telegram/catalog_url.json") as json_in:
        dat=json.load(json_in)
        catalog_address=dat["url_catalog"]

    r = requests.get(catalog_address+"/telegram_bot/settings")

    conf = r.json()


    token = conf["TG_Token"][0]
    flagID = 0
    #SimpleBot
    #bot = MyBot(token)

    # SimpleSwitchBot
    broker = conf["broker"]
    port = conf["port"]
    topic = conf["topic1"]
    #ssb = SimpleSwitchBot(token, broker, port, topic)
    
    
    sb=SwitchBot(token,broker,port,topic,catalog_address)
    while True:
        time.sleep(3)