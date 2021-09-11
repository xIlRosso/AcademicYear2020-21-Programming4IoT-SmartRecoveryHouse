import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import json, time
import requests
import telegramMethods as tm



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
        self.client = tm.MyMQTT.MyMQTT("telegramBot",broker,port,None)
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
        tmp_var='/'+name_field.pop(0)

        val_field = ""
        while name_field != []:
            val_field += "/" +name_field.pop(0)


        return tmp_var, val_field


    def on_chat_message(self, msg):
        content_type, chat_type, chat_ID = telepot.glance(msg)
        message = msg['text']
        global flagID
        global flagFolder
        
        r=requests.get(catalog_address+"/telegram_bot/pin_ids")
        pins = r.json()
        if flagFolder!=999:
            name_field, val_field=self.split_message(message)


        if message == "/start":
            self.bot.sendMessage(chat_ID, text='Please insert pin')
            
        elif message == "/options" and flagID == 1:
            buttons=[[InlineKeyboardButton(text=f'Med Folder', callback_data='/folder'),
                    InlineKeyboardButton(text=f'Simulations', callback_data='/Sim')]]
            keyboard= InlineKeyboardMarkup(inline_keyboard=buttons)

            self.bot.sendMessage(chat_ID, text='Select an option', reply_markup=keyboard)

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

        elif message == pins["Doctor_PIN"]:
            flagID = 1
            self.bot.sendMessage(chat_ID, text='Access granted, please write /options')

        elif name_field == '/addPatient':
            pObj = tm.PatientClass.Patient()
            frame = pObj.createFrame(val_field)
            pObj.sendFrame(catalog_address + "/telegram/addPatient", frame) #post request

        elif name_field == '/addPatientAddress':
            pObj = tm.PatientClass.Patient()
            frame = pObj.addAddress(val_field)
            pObj.updateFrame(catalog_address + "/telegram/updateAddress", frame) #put request

        elif name_field == '/addDoctor':
            dObj = tm.DoctorClass.Doctor()
            frame = dObj.createFrame(val_field)
            dObj.sendFrame(catalog_address + "/telegram/addDoctor", frame) #post request

        elif name_field == '/addCaretaker':
            cObj = tm.CaretakerClass.Caretaker()
            frame = cObj.createFrame(val_field)
            cObj.sendFrame(catalog_address + "/telegram/addCaretaker", frame) #post request

        elif name_field == '/updateActuator':
            pObj = tm.PatientClass.Patient()
            frame = pObj.updateActuatorVal(val_field)
            pObj.updateFrame(catalog_address + "/telegram/updateActuator", frame) #put request

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

if __name__ == "__main__":

    with open("catalog_mqtt_settings.json","r") as json_in:
        setsCatalog = json.load(json_in)

    S=tm.MQTT_telegram.Subscribers(setsCatalog["ID"], setsCatalog["topic"], setsCatalog["broker"], setsCatalog["port"])
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
    
    sb=SwitchBot(token,broker,port,topic,catalog_address)
    while True:
        time.sleep(3)