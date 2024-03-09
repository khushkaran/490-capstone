/*
PINOUT:
RC522 MODULE    Uno/Nano     MEGA
SDA             D10          D9
SCK             D13          D52
MOSI            D11          D51
MISO            D12          D50
IRQ             N/A          N/A
GND             GND          GND
RST             D9           D8
3.3V            3.3V         3.3V
*/
/* Include the standard Arduino SPI library */
#include <SPI.h>
/* Include the RFID library */
#include <RFID.h>

/* Define the DIO used for the SDA (SS) and RST (reset) pins. */
#define SDA_DIO 9
#define RESET_DIO 8
String key;
/* Create an instance of the RFID library */
RFID RC522(SDA_DIO, RESET_DIO); 

void setup()
{ 
  Serial.begin(9600);
  /* Enable the SPI interface */
  SPI.begin(); 
  /* Initialise the RFID reader */
  RC522.init();
}

char read;
void loop()
{
  /* Has a card been detected? */
  if (RC522.isCard())
  {
    /* If so then get its serial number */
    RC522.readCardSerial();
    Serial.println("Card detected:");
    
    for (int i = 0; i < 5; i++) {
      key += RC522.serNum[i];
    }

    Serial.println("hello");
    Serial.println(key);

    // Serial.print(rfid_key,DEC);
    if (key == "23823921923205") {
      Serial.write('aye');
      key = "";
    } else if (key == "23413422214535" ) {
      Serial.write('bee');
    } else {
      Serial.write('nothing');
    }
    // for(int i=0;i<5;i++)
    // {
    //   rfid_key = RC522.serNum[i];
    //   Serial.print(RC522.serNum[i],DEC);
    //   if(rfid_key == "238a239a219a23a205a") {
    //     Serial.print('a');
    //   } else if (rfid_key == "234a134a222a145a35a" ) {
    //     Serial.print('b');
    //   }
    //   else{
    //      Serial.write('nothing');
    //   }
      
    // }
    Serial.println();
    Serial.println();
  }
  delay(1000);
}
