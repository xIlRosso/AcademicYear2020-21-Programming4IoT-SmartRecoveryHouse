import json
import requests

class Caretaker():

    name = ""
    age = 0
    patientAssigned = ""

    def __init__(self):
        pass


    def buildAttributes(self, datum) -> None:
        datum_list = datum.split('/')
        datum_list.pop(0)

        self.name = datum_list.pop(0)
        self.age = int(datum_list.pop(0))
        self.patientAssigned = datum_list.pop(0)


    def createFrame(self) -> str:

        frame = {
            "name" : self.name,
            "age" : self.age,
            "patientAssigned" : self.patientAssigned
        }

        return json.dumps(frame)

    def sendFrame(self, ipAddress, frame):
        requests.post(ipAddress, frame)
