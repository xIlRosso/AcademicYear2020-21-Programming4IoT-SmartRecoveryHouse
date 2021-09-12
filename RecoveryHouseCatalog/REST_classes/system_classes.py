# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 18:56:07 2021

@author: ilros
"""

import json
import copy


class GET_manager(object):
    def __init__(self, path):
        self.path=path
        
    def run(self):

        if self.path[0]=='sensors':
            _set_path="settings.json"
            with open(_set_path) as json_file:
                data=json.load(json_file)
            
            if self.path[1]=='house':
                #we need to send the basic setup for the sensors of the house
                resp = {
                    "broker" : data["broker"],
                    "port" : data["port"],
                    "temperature" : data["meanAndVarSensorsHouse"]["temperature"],
                    "humidity" : data["meanAndVarSensorsHouse"]["humidity"],
                    "lumen" : data["meanAndVarSensorsHouse"]["lumen"]
                    }
                
                return json.dumps(resp)
                
                
            if self.path[1]=='house_list':
                resp = []
                
                if data["patientsList"]!=[]:
                    for patient in data["patientsList"]:
                        resp.append(patient["houseDevices"])
                    
                    return json.dumps(resp)
                #we need to get all the sensors from all the houses, publish on house-based topics
                

        elif self.path[0] == 'telegram':
            _set_path="settings.json"
            with open(_set_path) as json_file:
                data=json.load(json_file)
                
            if self.path[1] == 'get_pins':
                
                resp = {
                    "Patient": [],
                    "Doctor": [],
                    "Caretaker": []
                    }
                
                for patient in data["patientsList"]:
                    resp["Patient"].append({"uniqueID":patient["uniqueID"], "pin":patient["pin"]})
                    
                for doctor in data["doctorsList"]:
                    resp["Doctor"].append({"uniqueID":doctor["uniqueID"], "pin":doctor["pin"]})
                
                for caretaker in data["caretakersList"]:
                    resp["Caretaker"].append({"uniqueID":caretaker["uniqueID"], "pin":caretaker["pin"]})
                    
                return json.dumps(resp)


        elif self.path[0] == 'controls':
            _set_path="settings.json"
            with open(_set_path) as json_file:
                data=json.load(json_file)
                
            if self.path[1] == 'settings':
                
                resp = {
                    "broker" : data["broker"],
                    "port" : data["port"]
                    }
                
                return json.dumps(resp)
            
            elif self.path[1] == 'house_list':
                
                resp={
                    "houses" : []
                    }
                
                if data["patientsList"]!=[]:
                    for patient in data["patientsList"]:
                        resp["houses"].append({"houseDevices" : patient["houseDevices"], "actList" : patient["actuatorsList"]})
                        
                    
                return json.dumps(resp)

        if self.path[0]=='sensor':
            
            _set_path="settings.json"
            with open(_set_path) as json_file:
                data=json.load(json_file)
            
            # try:
            #     f=open(_set_path)
            # except IOError:
            #     return "Error 400 : No such sensor present in the Catalog"
            resp=0
            
            if self.path[1]=='patient':
                resp={
                    "broker" : data["broker"],
                    "port" : data["port"],
                    "devicesList" : [],
                    "Topics_List" : []
                    }
                for i in range(0,3):
                    resp['devicesList'].append(data['devicesList'][i])
                    resp["Topics_List"].append(data["Topics_List"]["patients"+str(i+1)])  
        
            elif self.path[1]=='housedev':
                resp={
                    "broker" : data["broker"],
                    "port" : data["port"],
                    "devicesList" : [],
                    "Topics_List" : []
                    }
                for i in range(0,3):
                    resp['devicesList'].append(data['devicesList'][3+i])
                    resp["Topics_List"].append(data["Topics_List"]["houses"+str(i+1)])
            else:
                return "Error 400 : There is no sensor such as the one requested"
            
            return json.dumps(resp)
        
        
        elif self.path[0]=='timecontr':
            
            _set_path="settings.json"
            
            with open(_set_path) as json_in:
                data=json.load(json_in)
            # data=json.load(open('settings.json'))
            if self.path[1]=='timeshift':
                resp={
                    "broker" : data['broker'],
                    "port" : data['port'],
                    "Topics_List" : [],
                    "Intervals" : data['Intervals']
                    }
                for i in range(1,len(resp["Intervals"])+1):
                    resp["Topics_List"].append(data['Topics_List']['tcsts'+str(i)])

                return json.dumps(resp)
            
            elif self.path[1]=='sensoract':
                resp={
                    "broker" : data['broker'],
                    "port" : data['port'],
                    "Topics_List" : [],
                    "sensors_to_sub_time_contr" : [],
                    "treshold_actuators" : {}
                    }
            
                resp["Topics_List"].append(data["Topics_List"]["tcslights"])
                resp["Topics_List"].append(data["Topics_List"]["tcsheating"])
                resp["Topics_List"].append(data["Topics_List"]["tcshumidifier"])
                resp["sensors_to_sub_time_contr"].append(data["Topics_List"]["houses1"])
                resp["sensors_to_sub_time_contr"].append(data["Topics_List"]["houses2"])
                resp["sensors_to_sub_time_contr"].append(data["Topics_List"]["houses3"])
                resp["treshold_actuators"] = data["tresholds_actuators"]
                
                return json.dumps(resp)
            
            
        elif self.path[0]=='trained_models':
            _set_path='data_comparison/trained_models.json'
            with open(_set_path) as json_in:
                data=json.load(json_in)
                
                return json.dumps(data)
                
        # for telegram bot basehost/telegram_bot/settings
        
        elif self.path[0]=='telegram_bot':
            _set_path="settings.json"
            
            with open(_set_path) as json_in:
                data=json.load(json_in)
                
            if self.path[1]=='settings':
                resp={
                    "TG_Token": data['TG_Token'],
                    "broker" : data['broker'],
                    "port" : data['port'],
                    "topic1" : data['Topics_List']['t_bot_topic'],
                    "topic2" : data['Topics_List']['sim_bot_topic']
                }
                
                return json.dumps(resp)
            
            elif self.path[1]=='pin_ids':
                resp={
                    "Doctor_PIN" : data["Pins"]["Doctor_PIN"],
                    "Caregiver_PIN" : data["Pins"]["Caregiver_PIN"],
                    "Patient_PIN" : data["Pins"]["Patient_PIN"]
                    }
                return json.dumps(resp)
            
            elif self.path[1]=='sens_measurements':
                resp={
                    "Temp" : data["Measurements_Patient"]["Temp"],
                    "HeartR" : data["Measurements_Patient"]["HeartR"],
                    "Weight" : data["Measurements_Patient"]["Weight"]
                    }
                return json.dumps(resp)

            elif self.path[1]=='house_measurements':
                resp={
                    "Temperature" : data["Measurements_House"]["Temperature"],
                    "LuminousIntensity" : data["Measurements_House"]["LuminousIntensity"],
                    "Humidity" : data["Measurements_House"]["Humidity"]
                    }
                return json.dumps(resp)

            elif self.path[1]=='actuators_status':
                resp={
                    "Actuator1" : data["Status_Actuators"]["Act1"],
                    "Actuator2" : data["Status_Actuators"]["Act2"],
                    "Heating" : data["Status_Actuators"]["Heating"],
                    "Humidifier" : data["Status_Actuators"]["Humidifier"],
                    "Lights" : data["Status_Actuators"]["Lights"]
                    }
                return json.dumps(resp)

            elif self.path[1]=='simulation_values':
                resp={
                    "Temp_sim" : data["Sim_settings"]["Temp_sim"],
                    "Weight_sim" : data["Sim_settings"]["Weight_sim"],
                    "HR_sim" : data["Sim_settings"]["HR_sim"],
                    "Temp_status" : data["Sim_settings"]["Temp_status"],
                    "HR_status" : data["Sim_settings"]["HR_status"],
                    "Weight" : data["Patient_Folder"]["Weight"]
                    }
                return json.dumps(resp)   

            elif self.path[1]=='patient_alarms':
                resp={
                    "Temp" : data["Alarms"]["Temp"],
                    "Weight" : data["Alarms"]["Weight"],
                    "HeartR" : data["Alarms"]["HeartR"]
                    }
                return json.dumps(resp)    
            
            
            elif self.path[1]=='regression_status':
                resp={
                    "Temp" : data["Regr_Values"]["Temp"],
                    "HeartR" : data["Regr_Values"]["HeartR"],
                    "Weight" : data["Regr_Values"]["Weight"]
                    }
                return json.dumps(resp)
            
            elif self.path[1]=="supported":
                resp = {
                    "actuators" : {},
                    "sensors" : {}
                    }
                
                resp["actuators"] = data["supportedActuators"]
                resp["sensors"] = data["supportedSensors"]
                
                return json.dumps(resp)
                
        elif self.path[0]=='thingspeak':
            _set_path="settings.json"
            
            with open(_set_path) as json_in:
                data=json.load(json_in)
                
            if self.path[1]=='settings':
                resp={
                    "broker" : data["broker"],
                    "port" : data["port"],
                    "Topics_List" : []
                    }
                
                for i in range(0,3):
                    resp["Topics_List"].append(data["Topics_List"]["patients"+str(i+1)])  
        
            return json.dumps(resp)
            
        else:
            return "Error 400 : The request cannot be fullfilled since the URL is wrong or it refers to something which does not exist"
    
class POST_manager():

    def __init__(self, path):
        self.path=path
        
    def run(self, data):
        if self.path[0]=='trained_modelsupdate':
            _set_path='data_comparison/trained_models.json'
            json.dump(data, open(_set_path,'w'))

        elif self.path[0]=='last_patient_measurement':
            _set_path="settings.json"            
            
            with open(_set_path) as json_in:
                sens_data=json.load(json_in)
            
            smt=dict(sens_data)
            smt["Measurements_Patient"]["Temp"] = data["Temp"]
            smt["Measurements_Patient"]["HeartR"] = data["HeartR"]
            smt["Measurements_Patient"]["Weight"] = data["Weight"]

            json.dump(smt, open(_set_path,'w'), indent=4)
        
        elif self.path[0]=='last_house_meas':
            _set_path="settings.json"            
            
            with open(_set_path) as json_in:
                sens_data=json.load(json_in)
            
            smt=dict(sens_data)
            smt["Measurements_House"]["Temperature"] = data["Temperature"]
            smt["Measurements_House"]["LuminousIntensity"] = data["LuminousIntensity"]
            smt["Measurements_House"]["Humidity"] = data["Humidity"]

            json.dump(smt, open(_set_path,'w'), indent=4)
            
        elif self.path[0]=='last_act_status':
            _set_path="settings.json"            
            
            with open(_set_path) as json_in:
                sens_data=json.load(json_in)
            
            smt=dict(sens_data)
            smt["Status_Actuators"]["Act1"] = data["Act1"]
            smt["Status_Actuators"]["Act2"] = data["Act2"]
            smt["Status_Actuators"]["Heating"] = data["Heating"]
            smt["Status_Actuators"]["Humidifier"] = data["Humidifier"]
            smt["Status_Actuators"]["Lights"] = data["Lights"]

            json.dump(smt, open(_set_path,'w'), indent=4)

        elif self.path[0]=='folder_patient':
            _set_path="settings.json"            
            
            with open(_set_path) as json_in:
                sens_data=json.load(json_in)
            
            smt=dict(sens_data)
            smt["Patient_Folder"]["Name"] = data["Name"]
            smt["Patient_Folder"]["Age"] = data["Age"]
            smt["Patient_Folder"]["Height"] = data["Height"]
            smt["Patient_Folder"]["Weight"] = data["Weight"]
            smt["Patient_Folder"]["Diagnostic"] = data["Diagnostic"]

            json.dump(smt, open(_set_path,'w'), indent=4)
        
        elif self.path[0]=='simulation_settings':
            _set_path="settings.json"            
            
            with open(_set_path) as json_in:
                sens_data=json.load(json_in)
            
            smt=dict(sens_data)
            smt["Sim_settings"]["Temp_sim"] = data["Temp_sim"]
            smt["Sim_settings"]["Weight_sim"] = data["Weight_sim"]
            smt["Sim_settings"]["HR_sim"] = data["HR_sim"]
            smt["Sim_settings"]["Temp_status"] = data["Temp_status"]
            smt["Sim_settings"]["HR_status"] = data["HR_status"]

            json.dump(smt, open(_set_path,'w'), indent=4)
        
        elif self.path[0]=='alarm_patient':
            _set_path="settings.json"            
            
            with open(_set_path) as json_in:
                sens_data=json.load(json_in)
            
            smt=dict(sens_data)
            smt["Alarms"]["Temp"] = data["Temp"]
            smt["Alarms"]["Weight"] = data["Weight"]
            smt["Alarms"]["HeartR"] = data["HeartR"]

            json.dump(smt, open(_set_path,'w'), indent=4)
            
        elif self.path[0] == 'regression_resultupdate':
            _set_path="settings.json"
            
            with open(_set_path) as json_in:
                sens_data=json.load(json_in)
            
            smt=dict(sens_data)
            smt["Regr_Values"]["Temp"] = data["Temp"]
            smt["Regr_Values"]["Weight"] = data["Weight"]
            smt["Regr_Values"]["HeartR"] = data["HeartR"]
            
            json.dump(smt, open(_set_path,'w'), indent=4)
            
        elif self.path[0]=="telegram":
            _set_path="settings.json"   
            with open(_set_path) as json_in:
                all_data=json.load(json_in)
            if self.path[1]=="addPatient":
                found = False
                if all_data["patientsList"] != []:
                    for patient in all_data["patientsList"]:
                        if data["uniqueID"] == patient["uniqueID"]:
                            found = True
                    
                if not found:
                    newPatient = copy.deepcopy(all_data["basePatient"])
                    
                    newPatient["name"] = data["name"]
                    newPatient["age"] = data["age"]
                    newPatient["uniqueID"] = data["uniqueID"]
                    newPatient["disease"] = data["disease"]
                    
                    for sens in data["bodySensors"]:
                        sens = sens.lower()
                        newSensor = copy.deepcopy(all_data["baseSensor"])
                        
                        newSensor["topic"] = all_data["baseTopic"] + "/" + newPatient["uniqueID"] + "/body/" 
                        newSensor["patientID"] = newPatient["uniqueID"]
                        newSensor["bn"] = newPatient["uniqueID"] + "/body/" + sens
                        newSensor["e"][0]["n"] = sens      
                        newSensor["e"][0]["u"] = all_data["supportedSensors"][sens]
                        
                        newPatient["bodyDevices"].append(newSensor)
                        newSensor = None
                        
                        
                    for sens in data["houseSensors"]:
                        sens = sens.lower()
                        newSensor = copy.deepcopy(all_data["baseSensor"])
                        
                        newSensor["topic"] = all_data["baseTopic"] + "/" + newPatient["uniqueID"] + "/house/"
                        newSensor["patientID"] = newPatient["uniqueID"]
                        newSensor["bn"] = newPatient["uniqueID"] + "/house/" + sens
                        newSensor["e"][0]["n"] = sens      
                        newSensor["e"][0]["u"] = all_data["supportedSensors"][sens]
                        
                        newPatient["houseDevices"].append(newSensor)
                        newSensor = None
                        
                    for actuator in data["controlledActuators"]:
                        actuator = actuator.lower()
                        newActuator = copy.deepcopy(all_data["baseActuator"])
                        
                        newActuator["topic"] = all_data["baseTopic"] + "/" + newPatient["uniqueID"] + "/actuator/"
                        newActuator["patientID"] = newPatient["uniqueID"]
                        newActuator["unit"] = all_data["supportedActuators"][actuator]
                        newActuator["name"] = actuator
                        newActuator["tresholds"].append(all_data["defaultActuatorValues"][actuator+"Low"]) 
                        newActuator["tresholds"].append(all_data["defaultActuatorValues"][actuator+"High"])
                        
                        newPatient["actuatorsList"].append(newActuator)
                        newActuator = None
                        
                    all_data["patientsList"].append(newPatient)
                json.dump(all_data, open(_set_path,"w"), indent=4)
                
            elif self.path[1]=="addDoctor":
                
                newDoctor = all_data["baseDoctor"].copy()
                found = False
                
                if all_data["doctorsList"] != []:
                    for doctor in all_data["doctorsList"]:
                        if doctor["uniqueID"] == data["uniqueID"]:
                            found = True
                
                if not found:
                    newDoctor["age"] = data["age"]
                    newDoctor["name"] = data["name"]
                    newDoctor["patientsAssigned"] = data["patientsAssigned"]
                    newDoctor["uniqueID"] = data["uniqueID"]
                    
                    all_data["doctorsList"].append(newDoctor)
                json.dump(all_data, open(_set_path,"w"), indent = 4)
                
            elif self.path[1]=="addCaretaker":
                
                newCaretaker = all_data["baseCaretaker"].copy()
                found = False
                
                if all_data["caretakersList"] != []:
                    for caretaker in all_data["caretakersList"]:
                        if caretaker["uniqueID"] == data["uniqueID"]:
                            found = True
                
                if not found:
                
                    newCaretaker["age"] = data["age"]
                    newCaretaker["name"] = data["name"]
                    newCaretaker["patientAssigned"] = data["patientAssigned"]
                    newCaretaker["uniqueID"] = data["uniqueID"]
                    
                    all_data["caretakersList"].append(newCaretaker)
                    
                json.dump(all_data, open(_set_path,"w"), indent = 4)
                
                
                    
                
class PUT_manager():
    def __init__(self, path):
        self.path=path
        
    def run(self, data):
        _set_path = "settings.json"
        with open(_set_path) as json_in:
            all_data=json.load(json_in)
            
        if self.path[0] == "telegram":
            if self.path[1] == "updateAddress":
                if all_data["patientsList"] != []:
                    for patient in all_data["patientsList"]:
                        if patient["uniqueID"] == data["uniqueID"]:
                            patient["address"] = data["address"]
                            
                    json.dump(all_data, open(_set_path, "w"), indent = 4)
                
            elif self.path[1] == "updateActuator":
                if all_data["patientsList"] != []:
                    for patient in all_data["patientsList"]:
                        if patient["uniqueID"] == data["uniqueID"]:
                            actList = patient["actuatorsList"]
                            for actuator in actList:
                                if actuator["name"] == data["actName"]:
                                    actuator["tresholds"][0]=data["actLow"]
                                    actuator["tresholds"][1]=data["actHigh"]
                                    
                    json.dump(all_data, open(_set_path,"w"), indent = 4)
                
            elif self.path[1] == "registerPatient":
                if all_data["patientsList"] != []:
                    for patient in all_data["patientsList"]:
                        if patient["uniqueID"] == data["userName"]:
                            patient["pin"] = data["pin"]
                            
                            
                    json.dump(all_data, open(_set_path,"w"), indent = 4)
                    
            elif self.path[1] == "registerDoctor":
                if all_data["doctorsList"] != []:
                    for doctor in all_data["doctorsList"]:
                        if doctor["uniqueID"] == data["userName"]:
                            doctor["pin"] = data["pin"]
                            
                    json.dump(all_data, open(_set_path,"w"), indent = 4)
                    
            elif self.path[1] == "registerCaretaker":
                if all_data["caretakersList"] != []:
                    for caretaker in all_data["caretakersList"]:
                        if caretaker["uniqueID"] == data["userName"]:
                            caretaker["pin"] = data["pin"]
                            
                    json.dump(all_data, open(_set_path,"w"), indent = 4)
            
                
class DELETE_manager():
    def __init__(self, path):
        self.path=path
        
    def run(self):
        _set_path = 'settings.json'
        with open(_set_path) as json_in:
            all_data=json.load(json_in)
        
        if self.path[0]=="telegram":
            if self.path[1]=="deletePatient":
                uniqueID = self.path[2]
                if all_data["patientsList"] != []:
                    i = 0
                    for patient in all_data["patientsList"]:
                        if patient["uniqueID"] == uniqueID:
                            all_data["patientsList"].pop(i)
                            
                        i+=1
                        
                    json.dump(all_data, open(_set_path,"w"), indent = 4)
                
            
            elif self.path[1]=="deleteDoctor":
                uniqueID = self.path[2]
                if all_data["doctorsList"] != []:
                    i = 0
                    for doctor in all_data["doctorsList"]:
                        if doctor["uniqueID"] == uniqueID:
                            all_data["doctorsList"].pop(i)
                            
                        i+=1
                        
                    json.dump(all_data, open(_set_path,"w"), indent = 4)
                    
            elif self.path[1]=="deleteCaretaker":
                uniqueID = self.path[2]
                if all_data["caretakersList"] != []:
                    i = 0
                    for caretaker in all_data["caretakersList"]:
                        if caretaker["uniqueID"] == uniqueID:
                            all_data["caretakersList"].pop(i)
                            
                        i+=1
                        
                    json.dump(all_data, open(_set_path,"w"), indent = 4)
        
