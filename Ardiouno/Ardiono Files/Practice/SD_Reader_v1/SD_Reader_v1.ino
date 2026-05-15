void setup() {
  // put your setup code here, to run once:
#include <SD.h>
#include <SPI.h>

// SD card chip select pin
#define CS_PIN 10

void setup() {
  // start serial monitor so we can see whats happening
  Serial.begin(9600);
  
  // try to initialize the SD card
  if (!SD.begin(CS_PIN)) {
    Serial.println("SD card failed to initialize!");
    return;
  }
  Serial.println("SD card initialized!");

  // create a file called data.txt and write to it
  File myFile = SD.open("data.txt", FILE_WRITE);
  
  if (myFile) {
    Serial.println("Writing to file...");
    myFile.println("Aiden Cheney - FSAE Data Logger - Summer 2026");
    myFile.close();
    Serial.println("Done!");
  } else {
    Serial.println("Error opening file!");
  }
}

void loop() {
  // put your main code here, to run repeatedly:

}
