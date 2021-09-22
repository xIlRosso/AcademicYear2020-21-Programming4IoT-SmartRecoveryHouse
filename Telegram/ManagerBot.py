import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import json, time
import requests
# import telegramMethods as tm
from telegramMethods.MyMQTT import *
from telegramMethods.MQTT_telegram import *
from telegramMethods.DoctorClass import *
from telegramMethods.CaretakerClass import *
from telegramMethods.PatientClass import *



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
        
        self.sims = {'Temp_sim': "",
                     'Weight_sim': "",
                     'HR_sim': "",
                     'Temp_status': "",
                     'HR_status': ""}

        self.folder = {'Name': "",
                       'Age': "",
                       'Height': "",
                       'Weight': "",
                       'Diagnostic': ""}
    
    

    def split_message(self, msg):
        name_field=msg.split('/')
        name_field.pop(0)
        tmp_var='/'+name_field.pop(0)

        val_field = ""
        while name_field != []:
            val_field += "/" +name_field.pop(0)


        return tmp_var, val_field

    def supportedFeatures(self) -> str:
        r=requests.get(catalog_address+"/telegram/supported")
        dicts = r.json()
        ansSupported = ""
        for key in dicts:
            ansSupported += key + ": "
            for keys in dicts[key]:
                ansSupported+= keys + ", "
            ansSupported += ". "
        
        return ansSupported

    def login(self, datum):
        global logged

        datum_list = datum.split('/')
        datum_list.pop(0)
        uniqueID = datum_list.pop(0)
        pw = datum_list.pop(0)

        r = requests.get(catalog_address + "/telegram/get_pins")
        pins = r.json()

        #response will be dict with "patients" : list of dict, "doc" : list of dict ecc

        for key in pins:
            for idpw in pins[key]:
                if idpw["uniqueID"] == uniqueID:
                    if idpw["pin"] == pw:
                        logged[key] = True

    def print_all_values(self, uniqueID) -> str:
        r = requests.get(catalog_address+"/telegram/getVals"+uniqueID)
        last_values = r.json()

        msg = ""

        name_unit = last_values["measUnit"]
        values = last_values["sensValues"]

        #last_values dict with correspondence between name sensor and unit
        #dict with "nameSensor" : value
        for key in values:
            msg += key + ": " + values[key] + " ["+name_unit[key]+"]\n"
            
        return msg

    def build_help(self) -> str:
        msg = ""
        msg+= "\t - /addSomeone\n"
        msg+= "\t - /updateField\n"
        msg+= "\t - /supported : shows list of supported actuators and sensors\n"
        msg+= "\t - /login : write the command + /uniqueID/password\n"
        msg+= "\t - /logout : everything logs out\n"
        msg+= "\t - /patientPinRegistration : write the command + /uniqueID/pin\n"
        msg+= "\t - /doctorPinRegistration : write the command + /uniqueID/pin\n"
        msg+= "\t - /caretakerPinRegistration : write the command + /uniqueID/pin\n"
        msg+= "\t - /deleteSomeone : to see how to delete someone\n"
        msg+= "\t - /patientValues : write the command + /uniqueID to see all the values of sensors and actuators\n"
        msg+= "\t - /removeSensor : write the command + /uniqueID/body/name_sensor ; body can be house if you want a house sensor, you need to be logged as a doctor\n"
        msg+= "\t - /addSensor : write the command + /uniqueID/body/name_sensor ; body can be house if you want a house sensor, you need to be logged as a doctor\n"
        msg+= "\t - /assignPatient : write the command + /uniqueIDdoctor/uniqueIDpatient\n"
        msg+= "\t - /assignPatientCaretaker : write the command + /uniqueCaretakerID/uniqueIDpatient\n"
        msg+= "\t - /updateHighlighted : write the command + /uniqueID"


        return msg


    def on_chat_message(self, msg):
        content_type, chat_type, chat_ID = telepot.glance(msg)
        message = msg['text']
        global logged
        global flagID
        global flagFolder
        with open("Telegram/explanation_messages.json") as json_in:
            explanations = json.load(json_in)
        
        

        # r=requests.get(catalog_address+"/telegram_bot/pin_ids")
        # pins = r.json()
        if flagFolder!=999:
            name_field, val_field=self.split_message(message)


        if message == "/start":
            self.bot.sendMessage(chat_ID, text='Welcome to the telegram bot')
            flagFolder = 3

        elif message == "/help":
            
            self.bot.sendMessage(chat_ID, text = self.build_help())

        elif message == "/addSomeone":
            buttons=[[InlineKeyboardButton(text=f'Patient', callback_data="/newPt"),
                    InlineKeyboardButton(text=f'Doctor', callback_data="/newDc"),
                    InlineKeyboardButton(text=f'Caretaker', callback_data="/newCt")]]

            keyboard= InlineKeyboardMarkup(inline_keyboard=buttons)
            self.bot.sendMessage(chat_ID, text="Select who do you want to add", reply_markup=keyboard)

        elif message == "/deleteSomeone":
            buttons=[[InlineKeyboardButton(text=f'Patient', callback_data="/delPt"),
                    InlineKeyboardButton(text=f'Doctor', callback_data="/delDc"),
                    InlineKeyboardButton(text=f'Caretaker', callback_data="/delCt")]]

            keyboard= InlineKeyboardMarkup(inline_keyboard=buttons)
            self.bot.sendMessage(chat_ID, text="Select who do you want to delete", reply_markup=keyboard)

        elif message == "/updateField":
            buttons=[[InlineKeyboardButton(text=f'PatientAddress', callback_data="/upPtAdd"),
                    InlineKeyboardButton(text=f'ActuatorTresh', callback_data="/upActTresh"),
                    InlineKeyboardButton(text=f'SimSettings', callback_data="/upSimSets"),
                    InlineKeyboardButton(text=f'Alarms', callback_data="/upAlarms")]]

            keyboard= InlineKeyboardMarkup(inline_keyboard=buttons)
            self.bot.sendMessage(chat_ID, text="Select what do you want to update", reply_markup=keyboard)

        elif message == "/newPt":
            self.bot.sendMessage(chat_ID, text = explanations["addPatient"] )

        elif message == "/newDc":
            self.bot.sendMessage(chat_ID, text = explanations["addDoctor"] )

        elif message == "/newCt":
            self.bot.sendMessage(chat_ID, text = explanations["addCaretaker"])

        elif message == "/upPtAdd":
            self.bot.sendMessage(chat_ID, text = explanations["addPatientAddress"])

        elif message == "/upActTresh":
            self.bot.sendMessage(chat_ID, text = explanations["updateActuator"])

        elif message == "/upSimSets":
            self.bot.sendMessage(chat_ID, text = explanations["updateSimSettings"])

        elif message == "/upAlarms":
            self.bot.sendMessage(chat_ID, text = explanations["updateAlarms"])

        elif message == "/delPt":
            self.bot.sendMessage(chat_ID, text = explanations["deletePatient"] )

        elif message == "/delDc":
            self.bot.sendMessage(chat_ID, text = explanations["deleteDoctor"] )

        elif message == "/delCt":
            self.bot.sendMessage(chat_ID, text = explanations["deleteCaretaker"])

        elif message == "/supported":
            self.bot.sendMessage(chat_ID, text = self.supportedFeatures())

        elif name_field == '/login':
            self.login(val_field)
            self.bot.sendMessage(chat_ID, text = json.dumps(logged))

        elif name_field == '/logout':
            logged["Patient"] = False
            logged["Doctor"] = False
            logged["Caretaker"] = False
            self.bot.sendMessage(chat_ID, text = json.dumps(logged))

        elif name_field == '/addPatient':
            pObj = Patient()
            pObj.buildAttributes(val_field)
            self.bot.sendMessage(chat_ID, text = json.dumps(pObj.bodySensors))
            self.bot.sendMessage(chat_ID, text = json.dumps(pObj.threshBSensors))
            frame = pObj.createFrame()
            pObj.sendFrame(catalog_address + "/telegram/addPatient", frame) #post request
            self.bot.sendMessage(chat_ID, text = json.dumps(frame))
            frame = 0

        elif name_field == '/addPatientAddress':
            pObj = Patient()
            frame = pObj.addAddress(val_field)
            pObj.updateFrame(catalog_address + "/telegram/updateAddress", frame) #put request
            frame = 0

        elif name_field == '/addDoctor':
            dObj = Doctor()
            dObj.buildAttributes(val_field)
            frame = dObj.createFrame()
            dObj.sendFrame(catalog_address + "/telegram/addDoctor", frame) #post request
            frame = 0

        elif name_field == '/addCaretaker':
            cObj = Caretaker()
            cObj.buildAttributes(val_field)
            frame = cObj.createFrame()
            cObj.sendFrame(catalog_address + "/telegram/addCaretaker", frame) #post request
            frame = 0

        elif name_field == '/updateSimulation':
            pObj = Patient()
            frame = pObj.updateSimsettings(val_field)
            pObj.updateFrame(catalog_address + "/telegram/updateSimulation", frame) #put request
            frame = 0

        elif name_field == '/updateAlarms':
            pObj = Patient()
            frame = pObj.updateAlarms(val_field)
            pObj.updateFrame(catalog_address + "/telegram/updateAlarms", frame) #put request
            frame = 0

        elif name_field == '/updateActuator':
            pObj = Patient()
            frame = pObj.updateActuatorVal(val_field)
            pObj.updateFrame(catalog_address + "/telegram/updateActuator", frame) #put request
            frame = 0

        elif name_field == '/patientPinRegistration':
            pObj = Patient()
            frame = pObj.registerAccount(val_field)
            pObj.updateFrame(catalog_address + "/telegram/registerPatient", frame)
            frame = 0

        elif name_field == '/doctorPinRegistration':
            dObj = Doctor()
            frame = dObj.registerAccount(val_field)
            dObj.updateFrame(catalog_address + "/telegram/registerDoctor", frame)
            frame = 0

        elif name_field == '/caretakerPinRegistration':
            cObj = Caretaker()
            frame = cObj.registerAccount(val_field)
            cObj.updateFrame(catalog_address + "/telegram/registerCaretaker", frame)
            frame = 0

        elif name_field == '/deletePatient':
            if logged["Doctor"]:
                pObj = Patient()
                pObj.deleteField(catalog_address + "/telegram/deletePatient"+val_field)
            else:
                self.bot.sendMessage(chat_ID, text = "Access Denied")

        elif name_field == '/deleteDoctor':
            if logged["Doctor"]:
                dObj = Doctor()
                dObj.deleteField(catalog_address + "/telegram/deleteDoctor"+val_field)
            else:
                self.bot.sendMessage(chat_ID, text = "Access Denied")

        elif name_field == '/deleteCaretaker':
            if logged["Doctor"]:
                cObj = Caretaker()
                cObj.deleteField(catalog_address + "/telegram/deleteCaretaker"+val_field)
            else:
                self.bot.sendMessage(chat_ID, text = "Access Denied")


        elif name_field == '/patientValues':

            resp = self.print_all_values(val_field)
            self.bot.sendMessage(chat_ID, text = resp)

        elif name_field == '/removeSensor':
            if logged["Doctor"]:
                pObj = Patient()
                pObj.deleteField(catalog_address + "/telegram/deleteSensor"+val_field)
            else:
                self.bot.sendMessage(chat_ID, text = "Access Denied")

        elif name_field == '/addSensor':
            if logged["Doctor"]:
                pObj = Patient()
                frame = pObj.addSensor(val_field)
                pObj.updateFrame(catalog_address+"/telegram/addSensor", frame)
            else:
                self.bot.sendMessage(chat_ID, text = "Access Denied")

        elif name_field == '/assignPatient':
            dObj = Doctor()
            frame = dObj.assignPatient(val_field)
            dObj.updateFrame(catalog_address + "/telegram/assignPatient", frame)

        elif name_field =='/assignPatientCaretaker':
            cObj = Caretaker()
            frame = cObj.assignPatient(val_field)
            cObj.updateFrame(catalog_address + "/telegram/assignPatientCaretaker", frame)

        elif name_field =='/updateHighlighted':
            pObj = Patient()
            frame = pObj.changeHighlighted(val_field)
            pObj.updateFrame(catalog_address + "/telegram/updateHighlighted", frame)


        else:
            self.bot.sendMessage(chat_ID, text="Command not supported, write /help for a list of commands")
        
        

    def on_callback_query(self,msg):
        query_ID, chat_ID, query_data = telepot.glance(msg,flavor='callback_query')  
        payload = self._message.copy() 
        payload['e'][0]['v'] = query_data
        payload['e'][0]['t'] = time.time()
        self.client.myPublish(self.topic, payload)
        global flagFolder
        message = msg['message']['text']
       
        if message == "Select an option":
            self.bot.sendMessage(chat_ID, text=f"Write {query_data}")
        elif message == "Fill the folder's patient, please write /folder followed by /name, /age, /height, /weight, /diagnostic and the field as /field. Click on the button Create Folder in order to activate input mode":
                flagFolder = query_data
        elif message == "Select a simulation to run":
            self.bot.sendMessage(chat_ID, text=query_data)
        elif message == "More Options":
            self.bot.sendMessage(chat_ID, text=query_data)
        elif message == "Select who do you want to add":
            self.bot.sendMessage(chat_ID, text = query_data)
        elif message == "Select what do you want to update":
            self.bot.sendMessage(chat_ID, text = query_data)
        elif message == "Select who do you want to delete":
            self.bot.sendMessage(chat_ID, text = query_data)

if __name__ == "__main__":

    with open("Telegram/catalog_mqtt_settings.json","r") as json_in:
        setsCatalog = json.load(json_in)

    S=Subscribers(setsCatalog["ID"], setsCatalog["topic"], setsCatalog["broker"], setsCatalog["port"])
    i=0
    while i<10:
        S.start()
        time.sleep(4)
        S.stop()
        i+=2

    with open("Telegram/catalog_url.json") as json_in:
        dat=json.load(json_in)
        catalog_address=dat["url_catalog"]

    r = requests.get(catalog_address+"/telegram/settings")

    conf = r.json()


    token = conf["TG_Token"][1]
    #SimpleBot
    #bot = MyBot(token)

    # SimpleSwitchBot
    broker = conf["broker"]
    port = conf["port"]
    topic = conf["topic_commands"]
    #ssb = SimpleSwitchBot(token, broker, port, topic)
    
    flagID=999
    flagFolder=999
    logged = {
        "Patient" : False,
        "Doctor" : False,
        "Caretaker" : False
    }
    
    sb=SwitchBot(token,broker,port,topic,catalog_address)
    while True:
        time.sleep(3)