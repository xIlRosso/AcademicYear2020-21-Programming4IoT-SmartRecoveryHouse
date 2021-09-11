import json
import requests

class Doctor:

    name = ""
    age = 0
    uniqueID = ""
    patientsAssigned = []


    def __init__(self):
        pass

    def buildAttributes(self, datum) -> None:
        datum_list = datum.split('/')
        datum_list.pop(0)

        self.name = datum_list.pop(0)
        self.age = int(datum_list.pop(0))
        self.uniqueID = datum_list.pop(0)

        if datum_list[0].lower() == "patientsassigned":
            datum_list.pop(0)

            while datum_list != []:
                self.patientsAssigned.append(datum_list.pop(0))

    def createFrame(self) -> dict:
        
        frame = {
            "name" : self.name,
            "age" : self.age,
            "patientsAssigned" : self.patientsAssigned,
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

    def sendFrame(self, ipAddress, frame) -> None:
        requests.post(ipAddress, json=frame)
        
    def updateFrame(self, ipAddress, frame) -> None:
        requests.put(ipAddress, json=frame)

    def deleteField(self, ipAddress, datum) -> None:
        datum_list = datum.split('/')
        datum_list.pop(0)

        requests.delete(ipAddress+'/'+datum_list.pop(0))