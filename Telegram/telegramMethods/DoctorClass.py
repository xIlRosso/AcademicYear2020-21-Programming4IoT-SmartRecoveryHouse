import json
import requests

class Doctor:

    name = ""
    age = 0
    patientsAssigned = []


    def __init__(self):
        pass

    def buildAttributes(self, datum) -> None:
        datum_list = datum.split('/')
        datum_list.pop(0)

        self.name = datum_list.pop(0)
        self.age = int(datum_list.pop(0))

        if datum_list[0].lower() == "patientsassigned":
            datum_list.pop(0)

            while datum_list != []:
                self.patientsAssigned.append(datum_list.pop(0))

    def createFrame(self) -> str:
        
        frame = {
            "name" : self.name,
            "age" : self.age,
            "patientsAssigned" : self.patientsAssigned
        }

        return json.dumps(frame)

    def sendFrame(self, ipAddress, frame):
        requests.post(ipAddress, frame)