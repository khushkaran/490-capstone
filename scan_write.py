import os.path
import csv

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

def check_if_tag_in_file(tag):
    with open("tag_characters.csv", "r") as character_file:
        character_reader = csv.reader(character_file)
        for row in character_reader:
            if row[0] == tag:
                return row[1]
    return -1

def append_tag_character_to_file(tag, character):
    with open("tag_characters.csv", "a", newline='') as character_file:
        character_writer = csv.writer(character_file)
        character_writer.writerow([tag, character])

if __name__ == '__main__':
    path = './tag_characters.csv'
    check_file = os.path.isfile(path)

    if (check_file == False):
        print("There is no character file yet. Creating one now")


    else:
        print("A character file with the name tag_characters.csv already exists. You can use this file or create a new one.")
        file_overwrite = input("Please enter 1 to delete the existing file and create a new one or 2 to use the old file.\n")

        if (file_overwrite == "1"):
            # f = open("tag_characters.csv", "w")
            with open("tag_characters.csv", "w", newline='') as character_file:
                character_writer = csv.writer(character_file, delimiter=',')
                character_writer.writerow(['Tag', 'Character'])

            print("A new character file has been created.")

            print("Please scan your tags one by one.")

            term = True
            while(term):
                data = rfid()
                # add the reading information here

                existing_character = check_if_tag_in_file(str(data))
                if (existing_character != -1):
                    print("This tag is alreaady associated with character " + existing_character + "; please scan a new tag.\n")
                else:
                    new_character = input("A new tag was detected. Please enter a name for this character.\n")
                    append_tag_character_to_file(str(data), new_character)
                    print("This tag is now associated with the following character: " + new_character)              

                term = input("Type STOP if you are done scanning. Otherwise, press any key to continue.\n")
                if (term == "STOP"):
                    term = False
                else:
                    term = True
        else:
            print("The old character file will be kept.")
            

    

    # need function to check if this tag is already in the file. 
    # need function to append the new pair to the end of the file. 

