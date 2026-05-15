#include <SdFat.h>
#include <SPI.h>

// SD card chip select pin
#define CS_PIN 10

// create SD object
SdFat SD;

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
  SdFile myFile;
  myFile.open("data.txt", O_WRITE | O_CREAT);
  
  if (myFile.isOpen()) {
    Serial.println("Writing to file...");
    myFile.println("Aiden Cheney - FSAE Data Logger - Summer 2026");
    myFile.close();
    Serial.println("Done!");
  } else {
    Serial.println("Error opening file!");
  }
}

void loop() {
  // nothing here, we only need to write the file once
}