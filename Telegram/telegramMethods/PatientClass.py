import json
import requests

class Patient:
    
    name = ""
    age = 0
    uniqueID = ""
    disease = ""
    bodySensors = []
    houseSensors = []
    controlledActuators = []
    

    def __init__(self):
        pass

    def buildAttributes(self, datum) -> None:
        datum_list = datum.split('/')
        self.name = datum_list.pop(0)
        self.age = int(datum_list.pop(0))
        self.uniqueID = datum_list.pop(0)
        self.disease = datum_list.pop(0)
        if datum_list[0].lower() == "bodysensors" : 
            datum_list.pop(0)
            while datum_list[0].lower() != "housesensors":
                self.bodySensors.append(datum_list.pop(0))
            datum_list.pop(0)
            while datum_list[0].lower() != "controlledactuators":
                self.houseSensors.append(datum_list.pop(0))
            datum_list.pop(0)
            while datum_list != []:
                self.controlledActuators.append(datum_list.pop(0))


    def createFrame(self) -> str:
        frame = {
            "name" : self.name,
            "age" : self.age,
            "uniqueID" : self.uniqueID,
            "disease" : self.disease,
            "bodySensors" : self.bodySensors,
            "houseSensors" : self.houseSensors,
            "controlledActuators" : self.controlledActuators
        }

        return json.dumps(frame)

    def addAddress(self, datum) -> str:
        datum_list = datum.split('/')
        self.uniqueID = datum_list.pop(0)
        address_list = datum_list.pop(0).split('_')
        address = ""
        while address_list != []:
            address += address_list.pop(0) + " "

        frame = {
            "uniqueID" : self.uniqueID,
            "address" : address
        }

        return json.dumps(frame)


    def sendFrame(self, ipAddress, frame) -> None:
        requests.post(ipAddress, frame)

    def sendAddress(self, ipAddress, frame) -> None:
        requests.put(ipAddress, frame)

    #maybe add put requests for updating fields
    