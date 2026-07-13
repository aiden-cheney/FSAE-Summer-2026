#include <Wire.h>

void setup() {
  Serial.begin(9600);
  delay(2000);
  Serial.println("Scanning I2C bus...");
  
  Wire.begin();
  
  for (byte address = 1; address < 127; address++) {
    Wire.beginTransmission(address);
    byte error = Wire.endTransmission();
    
    if (error == 0) {
      Serial.print("Device found at address 0x");
      Serial.println(address, HEX);
    }
  }
  Serial.println("Scan complete.");
}

void loop() {}