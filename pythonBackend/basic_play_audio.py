from csv import DictReader

from playsound import playsound  # need version 1.2.2
from serial import Serial
from queue import Queue
import threading
from queue import Empty
import requests

#reference: https:// stackoverflow.com / questions / 38861980 / attempting - to - read -from-two - serial - ports - at - once
rfid_reader_queue = Queue(1000)

serA = None
serB = None

BASE = "http://127.0.0.1:5000/"

serialPortsAssigned = False
threadingNotStarted = True

def serial_read(s, port_name):
    while True:
        try:
            line = s.readline().decode().strip()
            rfid_reader_queue.put((port_name, line))
        except Exception as e:
            print(f"Error reading from {port_name}: {e}")

def startThreading():
    global threadingNotStarted
    if (threadingNotStarted):
        threadA = threading.Thread(target=serial_read, args=(serA, "serA"))
        threadA.start()
        threadB = threading.Thread(target=serial_read,
                                    args=(serB, "serB"))
        threadB.start()
        threadingNotStarted = False
        print("starting threading")

def assignSerialPorts():

    global serA
    global serB

    if serA is None:
        # get serial ports from backend
        response = requests.get(BASE + "/ports")
        result = response.json()


        if result !=  []:
            # user has passed serial ports
            serA = Serial(result[0]['port'])
            serB = Serial(result[1]['port'])
            # serC = Serial(result[2])
            ## serD = Serial(result[3])
            print("done assigning ports")
            return True

        else:
            return False
    return True




while True:

    try:

        if assignSerialPorts():
            startThreading()

            port_name, tag = rfid_reader_queue.get(True, 1)
            name = str(tag+port_name)
            data = {"name": name, "tag": tag, "reader": port_name}

            # get tag and reader info from database
            response = requests.get(BASE + "/modifyChar", data)
            result = response.json()


            if (result == []):
                # there is no such tag and reader association in database
                response = requests.put(BASE + "/modifyChar", data)
                print(response.json())

            else:
                # there is such association, so it is being tapped again to play the sound
                soundFile = result['soundFile']

                if (soundFile != None):
                    # sound file exsist
                    playsound(soundFile)





    except Empty:
        pass

