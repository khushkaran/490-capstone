from playsound import playsound # need version 1.2.2

def rfid():
    import serial
    ser = serial.Serial()
    ser.baudrate = 9600
    try:
        ser.port = "COM3"
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

    if data == 23823921923205:
        print("hello")
        playsound('filea.mp3') 
        # audio = Path().cwd() / "filea.mp3"
        # playsound(audio)
    elif data == 23413422214535:
        playsound("fileb.mp3")
        # audio = Path().cwd() / "fileb.mp3"
        # playsound(audio)

