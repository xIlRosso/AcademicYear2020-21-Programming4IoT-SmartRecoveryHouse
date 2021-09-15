import json
import requests

class Patient:
    
    name = ""
    age = 0
    uniqueID = ""
    disease = ""
    bodySensors = []
    threshBSensors = []
    alarmbSensors = []
    houseSensors = []
    controlledActuators = []
    

    def __init__(self):
        pass

    def buildAttributes(self, datum) -> None:
        datum_list = datum.split('/')
        datum_list.pop(0)
        self.name = datum_list.pop(0)
        self.age = int(datum_list.pop(0))
        self.weight = int(datum_list.pop(0))
        self.uniqueID = datum_list.pop(0)
        self.disease = datum_list.pop(0)
        if datum_list[0].lower() == "bodysensors" : 
            datum_list.pop(0)
            while datum_list[0].lower() != "thresSensors":
                self.bodySensors.append(datum_list.pop(0))
            datum_list.pop(0)
            while datum_list[0].lower() != "alarmSensors":
                self.threshBSensors.append(float(datum_list.pop(0)))
            datum_list.pop(0)            
            while datum_list[0].lower() != "housesensors" :
                self.alarmbSensors.append(float(datum_list.pop(0)))
            datum_list.pop(0)
            while datum_list[0].lower() != "controlledactuators":
                self.houseSensors.append(datum_list.pop(0))
            datum_list.pop(0)
            while datum_list != []:
                self.controlledActuators.append(datum_list.pop(0))


    def createFrame(self) -> dict:

        thresDict = {
        }
        for keys in self.bodySensors:

            ind = self.bodySensors.index(keys)

            thresDict[keys+"Low"].append(self.threshBSensors[ind*2])
            thresDict[keys+"High"].append(self.threshBSensors[ind*2+1])
        alarmDict = {
        }
        for keys in self.alarmbSensors:

            ind = self.alarmbSensors.index(keys)

            alarmDict[keys+"Low"].append(self.alarmbSensors[ind*2])
            alarmDict[keys+"High"].append(self.alarmbSensors[ind*2+1])  

        frame = {
            "name" : self.name,
            "age" : self.age,
            "weight" : self.weight,
            "uniqueID" : self.uniqueID,
            "disease" : self.disease,
            "bodySensors" : self.bodySensors,
            "thresholds" : thresDict,
            "alarms" : alarmDict,
            "houseSensors" : self.houseSensors,
            "controlledActuators" : self.controlledActuators,
            "address" : ""
        }

        return frame

    def addAddress(self, datum) -> dict:
        datum_list = datum.split('/')
        datum_list.pop(0)
        self.uniqueID = datum_list.pop(0)
        address_list = datum_list.pop(0).split('_')
        address = ""
        while address_list != []:
            address += address_list.pop(0) + " "

        frame = {
            "uniqueID" : self.uniqueID,
            "address" : address
        }

        return frame

    def updateSimsettings(self, datum) -> dict:
        datum_list = datum.split('/')
        datum_list.pop(0)
        self.uniqueID = datum_list.pop(0)
        sensName = datum_list.pop(0)
        typeSim = datum_list.pop(0)
        statusSim = datum_list.pop(0)

        frame = {
            "uniqueID" : self.uniqueID,
            "sensorName" : sensName,
            "typeSim" : typeSim,
            "statusSim" : statusSim
        }

        return frame

    def updateAlarms(self, datum) -> dict:
        datum_list = datum.split('/')
        datum_list.pop(0)
        self.uniqueID = datum_list.pop(0)
        sensorName = datum_list.pop(0)
        alarmLow = datum_list.pop(0)
        alarmHigh = datum_list.pop(0)

        frame = {
            "uniqueID" : self.uniqueID,
            "sensorName" : sensorName,
            "alarmLow" : alarmLow,
            "alarmHigh" : alarmHigh
        }

        return frame

    def updateActuatorVal(self, datum) -> dict:
        datum_list = datum.split('/')
        datum_list.pop(0)
        self.uniqueID = datum_list.pop(0)
        actName = datum_list.pop(0)
        actLow = datum_list.pop(0)
        actHigh = datum_list.pop(0)

        frame = {
            "uniqueID" : self.uniqueID,
            "actName" : actName,
            "actLow" : actLow,
            "actHigh" : actHigh
        }

        return frame

    def registerAccount(self, datum) -> dict:
        datum_list = datum.split('/')
        datum_list.pop(0)

        frame = {
            "userName" : datum_list.pop(0),
            "pin" : datum_list.pop(0)
        }

        return frame

    def sendFrame(self, ipAddress, frame) -> None:
        requests.post(ipAddress, json=frame)

    def updateFrame(self, ipAddress, frame) -> None:
        requests.put(ipAddress, json=frame)

    def deleteField(self, ipAddress, datum) -> None:
        datum_list = datum.split('/')
        datum_list.pop(0)

        requests.delete(ipAddress+'/'+datum_list.pop(0))

    #maybe add put requests for updating fields
    