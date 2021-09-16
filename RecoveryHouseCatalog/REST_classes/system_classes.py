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
                
                
            elif self.path[1]=='house_list':
                resp = []
                
                if data["patientsList"]!=[]:
                    for patient in data["patientsList"]:
                        resp.append(patient["houseDevices"])
                    
                    return json.dumps(resp)
                #we need to get all the sensors from all the houses, publish on house-based topics
                
            elif self.path[1]=='bodydevices_list':
                resp = []
                
                if data["patientsList"]!=[]:
                    for patient in data["patientsList"]:
                        resp.append(patient["bodyDevices"])
                    
                    return json.dumps(resp)
                #we need to get all the sensors from all the houses, publish on house-based topics
                
            elif self.path[1]=='sim_values':
                
                resp = {}
                uniqueID = self.path[2]
                
                if data["patientsList"] != []:
                    for patient in data["patientsList"]:
                        if patient["uniqueID"] == uniqueID:
                            resp = patient["bodySensorsSimulation"]
                
                return json.dumps(resp)
            
            
            elif self.path[1]=='patient':
                
                resp = {
                    "broker" : data["broker"],
                    "port" : data["port"],
                    }
                
                return json.dumps(resp)
            
        elif self.path[0]=='thingspeak':
            _set_path="settings.json"
            with open(_set_path) as json_file:
                data=json.load(json_file)

            if self.path[1]=='settings':
                resp = {
                    "broker" : data["broker"],
                    "port" : data["port"],
                    "url" : data["thinkspeakSettings"]["tsURL"],
                    "key" : data["thinkspeakSettings"]["tsKEY"],
                    "clearURL" : data["thinkspeakSettings"]["tsCLEARURL"],
                    "field" : data["thinkspeakSettings"]["tsFields"]
                }
                return json.dumps(resp)

            if self.path[1]=='highlightedPatient':
                _set_path="settings.json"
                with open(_set_path) as json_file:
                    data=json.load(json_file)
            
                resp = data["highlightedPatient"]
                
                return json.dumps(resp)

            elif self.path[1]=="highlighted":

                resp = ""
                uniqueID = self.path[2]
                
                if data["patientsList"] != []:
                    for patient in data["patientsList"]:
                        if patient["uniqueID"] == uniqueID:
                            resp = patient["bodyDevices"][0]["topic"]
                
                return json.dumps(resp)

        elif self.path[0] == 'telegram':
            _set_path="settings.json"
            with open(_set_path) as json_file:
                data=json.load(json_file)
                
                
                
            if self.path[1]=='settings':
                resp={
                    "TG_Token": data['TG_Token'],
                    "broker" : data['broker'],
                    "port" : data['port'],
                    "topic_commands" : data['telegramTopics']['t_bot_topic'],
                    "topic_alarms" : data['telegramTopics']['sim_bot_topic']
                }
                
                return json.dumps(resp)
            
            
            elif self.path[1] == 'get_pins':
                
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
            
            
            elif self.path[1]=="supported":
                resp = {
                    "actuators" : {},
                    "sensors" : {}
                    }
                
                resp["actuators"] = data["supportedActuators"]
                resp["sensors"] = data["supportedSensors"]
                
                return json.dumps(resp)

            elif self.path[1]=="alarm_status":
                resp = []
                
                if data["patientsList"] != []:
                    resp = data["patientsList"]
                    
                    return json.dumps(resp)
                
            elif self.path[1]=='getVals':
                
                uniqueID = self.path[2]
                
                resp = {
                    "measUnit" : {},
                    "sensValues": {}
                    }
                
                resp["measUnit"] = data["correspondentUnits"]
                
                
                if data["patientsList"]!=[]:
                    for patient in data["patientsList"]:
                        if patient["uniqueID"] == uniqueID:
                            if patient["bodyDevices"] != []:
                                for sensor in patient["bodyDevices"]:
                                    resp["sensValues"].update({sensor["e"][0]["n"] : sensor["e"][0]["n"]})
                                    
                            if patient["houseDevices"] != []:
                                for sensor in patient["houseDevices"]:
                                    resp["sensValues"].update({sensor["e"][0]["n"] : sensor["e"][0]["n"]})
                                    
                            if patient["actuatorsList"] != []:
                                for actuator in patient["actuatorsList"]:
                                    resp["sensValues"].update({actuator["name"] : actuator["state"]})
                                    
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

            
        else:
            return "Error 400 : The request cannot be fullfilled since the URL is wrong or it refers to something which does not exist"
    
class POST_manager():

    def __init__(self, path):
        self.path=path
        
    def run(self, data):
        if self.path[0]=='trained_modelsupdate':
            _set_path='data_comparison/trained_models.json'
            json.dump(data, open(_set_path,'w'))
                
        elif self.path[0] == 'regression_resultupdate':
            _set_path="settings.json"
            
            with open(_set_path) as json_in:
                sens_data=json.load(json_in)
            
            smt=dict(sens_data)
            smt["Regr_Values"]["Temp"] = data["Temp"]
            smt["Regr_Values"]["Weight"] = data["Weight"]
            smt["Regr_Values"]["HeartR"] = data["HeartR"]
            
            json.dump(smt, open(_set_path,'w'), indent=4)
            
            
        elif self.path[0] == 'updateSens':
            _set_path="settings.json"   
            with open(_set_path) as json_in:
                all_data=json.load(json_in)
                
            if self.path[1] == 'body':
                
                uniqueID = self.path[2] 
                
                dev = data
                
                if all_data["patientsList"] != []:
                    for patient in all_data["patientsList"]:
                        if patient["uniqueID"] == uniqueID:
                            if patient["bodyDevices"] != []:
                                for sensor in patient["bodyDevices"]:
                                    if sensor["e"][0]["n"] == data["e"][0]["n"]:
                                        sensor["e"][0]["v"]=data["e"][0]["v"]
                                        
                    json.dump(all_data, open(_set_path,"w"), indent=4)
                    
            elif self.path[1] == 'house':
                
                uniqueID = self.path[2] 
                
                dev = data
                
                if all_data["patientsList"] != []:
                    for patient in all_data["patientsList"]:
                        if patient["uniqueID"] == uniqueID:
                            if patient["houseDevices"] != []:
                                for sensor in patient["houseDevices"]:
                                    if sensor["e"][0]["n"] == data["e"][0]["n"]:
                                        sensor["e"][0]["v"]=data["e"][0]["v"]
                                        
                    json.dump(all_data, open(_set_path,"w"), indent=4)
                
            elif self.path[1] == 'actuator':
                
                uniqueID = self.path[2] 
                
                dev = data
                
                if all_data["patientsList"] != []:
                    for patient in all_data["patientsList"]:
                        if patient["uniqueID"] == uniqueID:
                            if patient["actuatorsList"] != []:
                                for actuator in patient["actuatorsList"]:
                                    if actuator["name"] == data["name"]:
                                        actuator["state"] = data["state"]
                                        
                    json.dump(all_data, open(_set_path,"w"), indent=4)
        
            
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
                    newPatient["weight"] = data["weight"]
                    newPatient["uniqueID"] = data["uniqueID"]
                    newPatient["disease"] = data["disease"]
                    newPatient["bodySensorsSimulation"] = all_data["defaultSimValues"]
                    if all_data["highlightedPatient"] == "":
                        all_data["highlightedPatient"] = newPatient["uniqueID"]
                    
                    for sens in data["bodySensors"]:
                        sens = sens.lower()
                        newSensor = copy.deepcopy(all_data["baseSensor"])
                        tresh = {
                            sens+"Low" : data["thresholds"][sens+"Low"],
                            sens+"High" : data["thresholds"][sens+"High"]
                        }
                        newSensor["simThresholds"] = tresh
                        alarm = {
                            sens+"Low" : data["alarms"][sens+"Low"],
                            sens+"High" : data["alarms"][sens+"High"]
                        }
                        newSensor["alarmThresholds"] = alarm
                        newSensor["topic"] = all_data["baseTopic"] + "/" + newPatient["uniqueID"] + "/body"
                        newSensor["patientID"] = newPatient["uniqueID"]
                        newSensor["bn"] = newPatient["uniqueID"] + "/body/" + sens
                        newSensor["e"][0]["n"] = sens      
                        newSensor["e"][0]["u"] = all_data["supportedSensors"][sens]
                    
                        newPatient["bodyDevices"].append(newSensor)
                        newSensor = None
                        
                        
                    for sens in data["houseSensors"]:
                        sens = sens.lower()
                        newSensor = copy.deepcopy(all_data["baseSensor"])
                        
                        newSensor["topic"] = all_data["baseTopic"] + "/" + newPatient["uniqueID"] + "/house"
                        newSensor["patientID"] = newPatient["uniqueID"]
                        newSensor["bn"] = newPatient["uniqueID"] + "/house/" + sens
                        newSensor["e"][0]["n"] = sens      
                        newSensor["e"][0]["u"] = all_data["supportedSensors"][sens]
                        
                        newPatient["houseDevices"].append(newSensor)
                        newSensor = None
                        
                    for actuator in data["controlledActuators"]:
                        actuator = actuator.lower()
                        newActuator = copy.deepcopy(all_data["baseActuator"])
                        
                        newActuator["topic"] = all_data["baseTopic"] + "/" + newPatient["uniqueID"] + "/actuator"
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

            elif self.path[1] == "updateAlarms":
                if all_data["patientsList"] != []:
                    for patient in all_data["patientsList"]:
                        if patient["uniqueID"] == data["uniqueID"]:
                            sensorList = patient["bodyDevices"]
                            for alarm in sensorList:
                                if alarm["e"][0]["n"] == data["sensorName"]:
                                    alarm["alarmThresholds"][alarm["e"][0]["n"]+"Low"]=data["alarmLow"]
                                    alarm["alarmThresholds"][alarm["e"][0]["n"]+"High"]=data["alarmHigh"]
                                    
                    json.dump(all_data, open(_set_path,"w"), indent = 4)

            elif self.path[1] == "updateSimulation":
                if all_data["patientsList"] != []:
                    for patient in all_data["patientsList"]:
                        if patient["uniqueID"] == data["uniqueID"]:
                            simsList = patient["bodySensorsSimulation"]
                            for simulation in simsList:
                                if simulation["sensorName"] == data["sensorName"]:
                                    simulation["typeSim"] = data["typeSim"]
                                    simulation["statusSim"] = data["statusSim"]

                                    
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
                    
                    
            elif self.path[1] == "addSensor":
                uniqueID = data["uniqueID"]
                zone = data["zone"]
                sens_name = data["sensName"]
                
                
                sens = sens_name.lower()
                newSensor = copy.deepcopy(all_data["baseSensor"])
                
                newSensor["topic"] = all_data["baseTopic"] + "/" + uniqueID + "/house/"
                newSensor["patientID"] = uniqueID
                newSensor["bn"] = uniqueID + "/house/" + sens
                newSensor["e"][0]["n"] = sens      
                newSensor["e"][0]["u"] = all_data["supportedSensors"][sens]
                
                if all_data["patientsList"] != []:
                    for patient in all_data["patientsList"]:
                        if patient["uniqueID"] == uniqueID:
                            patient[zone+"Devices"].append(newSensor)
                            
                            
                    json.dump(all_data, open(_set_path, "w"), indent = 4)
                    
            elif self.path[1] == "assignPatient":
                docID = data["docID"]
                patID = data["patID"]
                
                if all_data["doctorsList"]!=[]:
                    for doctor in all_data["doctorsList"]:
                        if doctor["uniqueID"] == docID:
                            doctor["patientsAssigned"].append(patID)
                            
                            
                    json.dump(all_data, open(_set_path, "w"), indent = 4)
                    
            elif self.path[1] == "assignPatientCaretaker":
                careID = data["careID"]
                patID = data["patID"]
                
                if all_data["caretakersList"]!=[]:
                    for caretaker in all_data["caretakersList"]:
                        if caretaker["uniqueID"] == careID:
                            caretaker["patientAssigned"] = patID
                            
                            
                    json.dump(all_data, open(_set_path, "w"), indent = 4)
            
            elif self.path[1] == "updateHighlighted":
                upID = data["uniqueID"]
                
                all_data["highlightedPatient"] = upID
                
                json.dump(all_data, open(_set_path,"w"), indent = 4)
            
        elif self.path[0] == "sensors":
            if self.path[1] == "updateTimeVisited":
                
                uniqueID = self.path[2]
                sens_name = self.path[3]
                
                if all_data["patientsList"] != []:
                    for patient in all_data["patientsList"]:
                        if patient["bodyDevices"] != []:
                            for device in patient["bodyDevices"]:
                                if uniqueID == device["patientID"]:
                                    if device["e"][0]["n"] == sens_name:
                                        device["timesVisited"] = data["timesVisited"]
                                    
                    json.dump(all_data, open(_set_path,"w"), indent = 4)
                    
            elif self.path[1] == "alarm_patient":
                
                uniqueID = self.path[2]
                sens_name = self.path[3]
                
                if all_data["patientsList"] != []:
                    for patient in all_data["patientsList"]:
                        if patient["uniqueID"] == uniqueID:
                            for key in data:
                                if data[key]!="":
                                    patient["alarms_patient"] = key
                                    
                    json.dump(all_data, open(_set_path, "w"), indent = 4)
            
                
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
                            if patient["uniqueID"] == all_data["highlightedPatient"]:
                                all_data["highlightedPatient"] = ""
                            
                        i+=1
                        
                if all_data["doctorsList"] != []:
                    i = 0
                    for doctor in all_data["doctorsList"]:
                        for patient_assigned in doctor["patientsAssigned"]:
                            if patient_assigned["uniqueID"] == uniqueID:
                                all_data["doctorsList"]["patientsAssigned"].pop(i)
                                
                            i+=1
                            
                            
                if all_data["caretakersList"] != []:
                    i = 0
                    for caretaker in all_data["caretakersList"]:
                        if caretaker["patientAssigned"] == uniqueID:
                            all_data["caretakersList"]["patientAssigned"] = ""
                            
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
        
            elif self.path[1] == "deleteSensor":
                uniqueID=self.path[2]
                zone = self.path[3]
                sens_name = self.path[4]
                
                if all_data["patientsList"] != []:
                    for patient in all_data["patientsList"]:
                        if patient["uniqueID"] == uniqueID:
                            if patient[zone+"Devices"] != []:
                                for sensor in patient[zone+"Devices"]:
                                    if sensor["e"][0]["n"]==sens_name:
                                        patient[zone+"Devices"].pop(patient[zone+"Devices"].index(sensor))
                                        
                    json.dump(all_data, open(_set_path, "w"), indent = 4)