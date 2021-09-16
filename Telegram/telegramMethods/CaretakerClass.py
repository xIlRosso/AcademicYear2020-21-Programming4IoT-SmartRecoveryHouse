import json
import requests

class Caretaker():

    name = ""
    age = 0
    uniqueID = ""
    patientAssigned = ""

    def __init__(self):
        pass


    def buildAttributes(self, datum) -> None:
        datum_list = datum.split('/')
        datum_list.pop(0)

        self.name = datum_list.pop(0)
        self.age = int(datum_list.pop(0))
        self.uniqueID = datum_list.pop(0)
        self.patientAssigned = datum_list.pop(0)


    def createFrame(self) -> dict:

        frame = {
            "name" : self.name,
            "age" : self.age,
            "patientAssigned" : self.patientAssigned,
            "uniqueID" : self.uniqueID
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

    def assignPatient(self, datum) -> dict:
        
        datum_list=datum.split('/')
        datum_list.pop(0)

        careID = datum_list.pop(0)
        patID = datum_list.pop(0)
        
        frame = {
            "careID" : careID,
            "patID" : patID
        }

        return frame

    def sendFrame(self, ipAddress, frame) -> None:
        requests.post(ipAddress, json=frame)

    def updateFrame(self, ipAddress, frame) -> None:
        requests.put(ipAddress, json=frame)

    def deleteField(self, ipAddress) -> None:
        requests.delete(ipAddress)