
#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN 9     
#define SS_PIN  10 

int nuid[4];       

MFRC522 mfrc522(SS_PIN, RST_PIN);

void setup() {
  Serial.begin(9600); 
  while (!Serial);    
  SPI.begin();      
  mfrc522.PCD_Init();   

}

void loop() {

  if ( ! mfrc522.PICC_IsNewCardPresent()) {
    return;
  }

  
  if ( ! mfrc522.PICC_ReadCardSerial()) {
    return;
  }


        for (byte i = 0; i < 4; i++)
        {
          nuid[i] = mfrc522.uid.uidByte[i];
          Serial.print(nuid[i] < 0x10 ? "0" : ""); 
          Serial.print(nuid[i],HEX);
        }
            
        
        
  

    mfrc522.PICC_HaltA();
    mfrc522.PCD_StopCrypto1();
}
