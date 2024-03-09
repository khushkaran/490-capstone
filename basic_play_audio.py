from playsound import playsound
import os
import serial

ser = serial.Serial('COM3', 9600, timeout=0)

while 1:
    x = ser.read()
    
    if x == 'aye':
        print("hello")
        playsound('filea.mp3')
    if x == 'bee':
        playsound('fileb.mp3')
    else:
        pass
