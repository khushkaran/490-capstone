from csv import DictReader

#from playsound import playsound  # need version 1.2.2
from serial import Serial
from queue import Queue
import threading
from queue import Empty
import requests

#reference: https:// stackoverflow.com / questions / 38861980 / attempting - to - read -from-two - serial - ports - at - once
rfid_reader_queue = Queue(1000)

serA = Serial("/dev/cu.usbmodem141101")
serB = Serial("/dev/cu.usbmodem141201")

def serial_read(s, port_name):
    while True:
        try:
            line = s.readline().decode().strip()
            rfid_reader_queue.put((port_name, line))
        except Exception as e:
            print(f"Error reading from {port_name}: {e}")

threadA = threading.Thread(target=serial_read, args=(serA, "serA"))
threadA.start()
threadB = threading.Thread(target=serial_read, args=(serB, "serB"))
threadB.start()

BASE = "http://127.0.0.1:5000/"

while True:

    try:
        port_name, tag = rfid_reader_queue.get(True, 1)
        # from csv we find the row that has same port and tag as read and play audio associated with it


        #print(tag+port_name)
        data = {"name": str(tag+port_name), "tag": tag, "reader": port_name}
        #print(data)
        response = requests.put(BASE + "/addChar/" + str(tag + port_name), data)
        print(response.json())

        input()
        #addChar/942022212782serA
        response = requests.get(BASE + "/getAllChar")
        print(response.json())





    except Empty:
        pass

