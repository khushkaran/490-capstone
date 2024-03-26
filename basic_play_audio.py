from csv import DictReader

from playsound import playsound  # need version 1.2.2
from serial import Serial
from queue import Queue
import threading
from queue import Empty

#reference: https:// stackoverflow.com / questions / 38861980 / attempting - to - read -from-two - serial - ports - at - once
rfid_reader_queue = Queue(1000)

serA = Serial("/dev/cu.usbmodem142301")
serB = Serial("/dev/cu.usbmodem142201")

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


while True:

    try:
        port_name, tag = rfid_reader_queue.get(True, 1)
        # from csv we find the row that has same port and tag as read and play audio associated with it

        #print(f"Reading from {port_name}: {tag}")

        with open("sound_associations.csv", 'r') as f:
            dict_reader = DictReader(f)
            list_of_dict = list(dict_reader)


        for row in list_of_dict:
            if row['Tag'] == tag and row['Reader'] == port_name:
                playsound("./sounds/"+ row['Sound'])




    except Empty:
        pass

