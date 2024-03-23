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
        print(f"Reading from {port_name}: {tag}")

        if port_name == "serA" and tag == "21814241145236":
            playsound('fileb.mp3')

        if port_name == "serB" and tag == "21814241145236":
            playsound('filea.mp3')

    except Empty:
        pass



"""
def rfid():

    ser = Serial()
    ser.baudrate = 9600

    ser2 = Serial()
    ser2.baudrate = 9600

    try:
        ser.port = "/dev/cu.usbmodem142301"
        ser2.port = "/dev/cu.usbmodem142201"

    except:
        print("error")

    ser.open()
    ser2.open()

    RFID_Data = ser.readline()
    RFID_Data2 = ser2.readline()
    if RFID_Data:
        RFID_Data = RFID_Data.decode()  # Decode arduino Serial
        RFID_Data = RFID_Data.strip()  # Strip Arduino Data to remove string
        RFID_Data = int(RFID_Data);  # Convert the Data to Int

    if RFID_Data2:
        RFID_Data2 = RFID_Data2.decode()  # Decode arduino Serial
        RFID_Data2 = RFID_Data2.strip()  # Strip Arduino Data to remove string
        RFID_Data2 = int(RFID_Data2);  # Convert the Data to Int

    return RFID_Data, RFID_Data2



while (True):
    # input ports that the readers are connected to
    data = rfid()
    print(data)

  
    if data == 21814241145236:
        print("reading" +  " " + str(data) + " " + "from reader /dev/cu.usbmodem142301")
        # playsound('fileb.mp3')
        # audio = Path().cwd() / "filea.mp3"
        # playsound(audio)
    elif data == 942022212782:
        print("reading" + " " + str(data) + " " + "from reader /dev/cu.usbmodem142301")
        # playsound("filea.mp3")
        # audio = Path().cwd() / "fileb.mp3"
        # playsound(audio)

    elif data2 == 21814241145236:
        print("reading" + str(data2) + "from reader /dev/cu.usbmodem142201")

    elif data2 == 942022212782:
        print("reading" + str(data2) + "from reader /dev/cu.usbmodem142201")

    else:
        print("error")
    """
