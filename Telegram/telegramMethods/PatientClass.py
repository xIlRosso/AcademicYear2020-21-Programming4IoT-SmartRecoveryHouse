import json
import requests

class Patient:
    
    name = ""
    age = ""
    uniqueID = ""
    bodySensors = []
    houseSensors = []
    controlledActuators = []
    

    def __init__(self):
        pass

    def buildAttributes(self, datum) -> None:
        datum_list = datum.split('/')
        self.name = datum_list.pop(0)
        self.age = datum_list.pop(0)
        self.uniqueID = datum_list.pop(0)
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
            "name" : "",
            "age" : "",
            "uniqueID" : "",
            "bodySensors" : [],
            "houseSensors" : [],
            "controlledActuators" : []
        }

        frame["name"] = self.name
        frame["age"] = self.age
        frame["uniqueID"] = self.uniqueID
        frame["bodySensors"] = self.bodySensors
        frame["houseSensors"] = self.houseSensors
        frame["controlledActuators"] = self.controlledActuators

        return json.dumps(frame)

    
    def sendFrame(self, address, frame) -> None:
        requests.post(address, frame)


    #maybe add put requests for updating fields
    