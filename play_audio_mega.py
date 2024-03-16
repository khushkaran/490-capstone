from playsound import playsound # need version 1.2.2
from serial import Serial

def rfid():

    ser = Serial()
    ser.baudrate = 9600
    try:
        ser.port = "/dev/cu.usbmodem142201"
    except:
        print("error")


    ser.open()
    RFID_Data=ser.readline()
    if RFID_Data:
        RFID_Data = RFID_Data.decode()  #Decode arduino Serial
        RFID_Data = RFID_Data.strip()   #Strip Arduino Data to remove string
        RFID_Data=int(RFID_Data);       #Convert the Data to Int
        return(RFID_Data)


while(True):
    data = rfid()
    print(data)

    if data == 21814241145236:
        playsound('filea.mp3') # change audioo that corresponds to tag for each reader
        # audio = Path().cwd() / "filea.mp3"
        # playsound(audio)
    elif data == 942022212782:
        playsound("fileb.mp3")
        # audio = Path().cwd() / "fileb.mp3"
        # playsound(audio)

