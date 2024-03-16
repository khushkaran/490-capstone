from playsound import playsound # need version 1.2.2
from serial import Serial
import csv
# Import writer class from csv module
from csv import writer
def createFile():
    return open("tags_to_character.csv", "w")

def setUp():

    try:
        return open("tags_to_character.csv", "a")

    except:
        return createFile()




def rfid():

    ser = Serial()
    ser.baudrate = 9600
    try:
        ser.port = "/dev/cu.usbmodem142101"
    except:
        print("error")


    ser.open()
    RFID_Data=ser.readline()
    if RFID_Data:
        RFID_Data = RFID_Data.decode()  #Decode arduino Serial
        RFID_Data = RFID_Data.strip()   #Strip Arduino Data to remove string
        RFID_Data=int(RFID_Data);       #Convert the Data to Int
        return(RFID_Data)

def checkIfTagRegistered(csvfile, tag):

    tagToCharacterReader = csv.reader(csvfile, delimiter=',')
    
    for row in tagToCharacterReader:
        if tag == row[0]:
            print("Character assigned to tag is: " + row[1])
            charChange = input("Would you like to change the Character assigned to this tag?[Y/N]")
            if charChange == "N":
                return
            elif charChange == "Y":
                charName = input("New Character Name: ")
                if (charName) == "Exit":
                    return
                return
            elif charChange == "Exit":
                return
            else:
                return


        else:
            print("No character registered for this tag")
            charName = input("Character Name: ")
            if charName == "Exit":
                return

            writer_object = writer(tagToCharacterReader)

            # Pass the list as an argument into
            # the writerow()
            writer_object.writerow([tag,charName])






while(True):

    data = rfid() # readings the tag
    print(data)
    fd = setUp()
    print("At any time type Exit to quit")
    checkIfTagRegistered(fd, data)
    input()






