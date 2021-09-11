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
    
    def send_simulations(self,a,b,Sens_name):
        if Sens_name == "Temp_sim":
            self.sims[Sens_name] = a
            self.sims["Temp_status"] = b
        elif Sens_name == "HR_sim": 
            self.sims[Sens_name] = a
            self.sims["HR_status"] = b 
        else:
            self.sims[Sens_name] = a
        requests.post(catalog_address+"/simulation_settings", json=self.sims)
        return("Simulation started")

    def split_message(self, msg):
        name_field=msg.split('/')
        name_field.pop(0)
        tmp_var='/'+name_field.pop(0)

        val_field = ""
        while name_field != []:
            val_field += "/" +name_field.pop(0)


        return tmp_var, val_field

    def supportedFeatures(self) -> str:
        r=requests.get(catalog_address+"/telegram_bot/supported")
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
            
        # elif message == "/options" and flagID == 1:
        #     buttons=[[InlineKeyboardButton(text=f'Med Folder', callback_data='/folder'),
        #             InlineKeyboardButton(text=f'Simulations', callback_data='/Sim')]]
        #     keyboard= InlineKeyboardMarkup(inline_keyboard=buttons)

        #     self.bot.sendMessage(chat_ID, text='Select an option', reply_markup=keyboard)

        # elif message == "/folder" and flagID == 1:
        #     buttons=[[InlineKeyboardButton(text=f'Create Folder', callback_data=1)]]
        #     keyboard= InlineKeyboardMarkup(inline_keyboard=buttons)

        #     self.bot.sendMessage(chat_ID, text="Fill the folder's patient, please write /folder followed by /name, /age, /height, /weight, /diagnostic and the field as /field. Click on the button Create Folder in order to activate input mode", reply_markup=keyboard)
    

        elif message == "/Sim" and flagID == 1:
            buttons=[[InlineKeyboardButton(text=f'Temp Fever', callback_data=self.send_simulations("r","y","Temp_sim")),
                    InlineKeyboardButton(text=f'Normal Temp', callback_data=self.send_simulations("r","n","Temp_sim")),
                    InlineKeyboardButton(text=f'Low Temp', callback_data=self.send_simulations("l","n","Temp_sim"))]]
            buttons2=[[InlineKeyboardButton(text=f'High Temp', callback_data=self.send_simulations("h","n","Temp_sim")),
                    InlineKeyboardButton(text=f'Normal Weight', callback_data=self.send_simulations("r","n","Weight_sim")),
                    InlineKeyboardButton(text=f'Low Weight', callback_data=self.send_simulations("l","n","Weight_sim"))]]
                    # InlineKeyboardButton(text=f'Next Options', callback_data="next_one"]]
            buttons3=[[InlineKeyboardButton(text=f'High Weight', callback_data=self.send_simulations("h","n","Weight_sim")),
                    InlineKeyboardButton(text=f'Normal HR', callback_data=self.send_simulations("r","n","HR_sim")),
                    InlineKeyboardButton(text=f'Low HR (HA)', callback_data=self.send_simulations("l","y","HR_sim"))]]
            buttons4=[[
                    InlineKeyboardButton(text=f'Low HR', callback_data=self.send_simulations("l","n","HR_sim")),
                    InlineKeyboardButton(text=f'High HR (HA)', callback_data=self.send_simulations("h","y","HR_sim")),
                    InlineKeyboardButton(text=f'High HR', callback_data=self.send_simulations("h","n","HR_sim"))]]
            keyboard= InlineKeyboardMarkup(inline_keyboard=buttons)
            keyboard2= InlineKeyboardMarkup(inline_keyboard=buttons2)
            keyboard3= InlineKeyboardMarkup(inline_keyboard=buttons3)
            keyboard4= InlineKeyboardMarkup(inline_keyboard=buttons4)
            

            self.bot.sendMessage(chat_ID, text="Select a simulation to run", reply_markup=keyboard)
            self.bot.sendMessage(chat_ID, text="More options", reply_markup=keyboard2)
            self.bot.sendMessage(chat_ID, text="More options", reply_markup=keyboard3)
            self.bot.sendMessage(chat_ID, text="More options", reply_markup=keyboard4)

        # elif message == pins["Doctor_PIN"]:
        #     flagID = 1
        #     self.bot.sendMessage(chat_ID, text='Access granted, please write /options')

        elif message == "/addSomeone":
            buttons=[[InlineKeyboardButton(text=f'Patient', callback_data="/newPt"),
                    InlineKeyboardButton(text=f'Doctor', callback_data="/newDc"),
                    InlineKeyboardButton(text=f'Caretaker', callback_data="/newCt")]]

            keyboard= InlineKeyboardMarkup(inline_keyboard=buttons)
            self.bot.sendMessage(chat_ID, text="Select who do you want to add", reply_markup=keyboard)

        elif message == "/updateField":
            buttons=[[InlineKeyboardButton(text=f'PatientAddress', callback_data="/upPtAdd"),
                    InlineKeyboardButton(text=f'ActuatorTresh', callback_data="/upActTresh")]]

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
            frame = pObj.createFrame()
            pObj.sendFrame(catalog_address + "/telegram/addPatient", frame) #post request
            self.bot.sendMessage(chat_ID, text = json.dumps(frame))

        elif name_field == '/addPatientAddress':
            pObj = Patient()
            frame = pObj.addAddress(val_field)
            pObj.updateFrame(catalog_address + "/telegram/updateAddress", frame) #put request

        elif name_field == '/addDoctor':
            dObj = Doctor()
            dObj.buildAttributes(val_field)
            frame = dObj.createFrame()
            dObj.sendFrame(catalog_address + "/telegram/addDoctor", frame) #post request

        elif name_field == '/addCaretaker':
            cObj = Caretaker()
            cObj.buildAttributes(val_field)
            frame = cObj.createFrame()
            cObj.sendFrame(catalog_address + "/telegram/addCaretaker", frame) #post request

        elif name_field == '/updateActuator':
            pObj = Patient()
            frame = pObj.updateActuatorVal(val_field)
            pObj.updateFrame(catalog_address + "/telegram/updateActuator", frame) #put request

        elif name_field == '/patientPinRegistration':
            pObj = Patient()
            frame = pObj.registerAccount(val_field)
            pObj.updateFrame(catalog_address + "/telegram/registerPatient", frame)

        elif name_field == '/doctorPinRegistration':
            dObj = Doctor()
            frame = dObj.registerAccount(val_field)
            dObj.updateFrame(catalog_address + "/telegram/registerDoctor", frame)

        elif name_field == '/caretakerPinRegistration':
            cObj = Caretaker()
            frame = cObj.registerAccount(val_field)
            cObj.updateFrame(catalog_address + "/telegram/registerCaretaker", frame)

        elif name_field == '/deletePatient':
            if logged["Doctor"]:
                pObj = Patient()
                pObj.deleteField(catalog_address + "/telegram/deletePatient",val_field)
            else:
                self.bot.sendMessage(chat_ID, text = "Access Denied")

        elif name_field == '/deleteDoctor':
            if logged["Doctor"]:
                dObj = Doctor()
                dObj.deleteField(catalog_address + "/telegram/deleteDoctor",val_field)
            else:
                self.bot.sendMessage(chat_ID, text = "Access Denied")

        elif name_field == '/deleteCaretaker':
            if logged["Doctor"]:
                cObj = Caretaker()
                cObj.deleteField(catalog_address + "/telegram/deleteCaretaker",val_field)
            else:
                self.bot.sendMessage(chat_ID, text = "Access Denied")

        

        # elif name_field == '/folder/name':
        #     # message=val_field
        #     self.folder['Name'] = val_field
        #     #/folder/name/Giovanni
        # elif name_field == '/folder/age' :
        #     self.folder['Age'] = val_field
        # elif name_field == '/folder/height' :
        #     self.folder['Height'] = val_field
        # elif name_field == '/folder/weight' :
        #     self.folder['Weight'] = val_field                        
        # elif name_field == '/folder/diagnostic' :
        #     self.folder['Diagnostic'] = val_field
        #     requests.post(catalog_address+"/folder_patient", json=self.folder)
        #     flagFolder=999

        else:
            self.bot.sendMessage(chat_ID, text="Command not supported")
        
        

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

    r = requests.get(catalog_address+"/telegram_bot/settings")

    conf = r.json()


    token = conf["TG_Token"][1]
    #SimpleBot
    #bot = MyBot(token)

    # SimpleSwitchBot
    broker = conf["broker"]
    port = conf["port"]
    topic = conf["topic2"]
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