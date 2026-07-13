#include <Wire.h>
#include <MPU6050.h>
#include <SdFat.h>
#include <SPI.h>
#include <SoftwareSerial.h>
#include <TinyGPSPlus.h>

MPU6050 mpu;
SdFat SD;
SoftwareSerial gpsSerial(2, 3);
TinyGPSPlus gps;

#define CS_PIN 10

void setup() {
  Serial.begin(9600);
  Wire.begin();
  gpsSerial.begin(9600);

  mpu.initialize();
  mpu.setFullScaleAccelRange(MPU6050_ACCEL_FS_2);
  Serial.println("MPU6050 ready!");

  if (!SD.begin(CS_PIN)) {
    Serial.println("SD card failed!");
    return;
  }
  Serial.println("SD card ready!");

  SdFile myFile;
  myFile.open("unified.csv", O_WRITE | O_CREAT | O_APPEND);
  myFile.println("time,lat,lng,x_g,y_g,z_g");
  myFile.close();
}

void loop() {
  // read GPS
  while (gpsSerial.available() > 0) {
    gps.encode(gpsSerial.read());
  }

  // read MPU
  int16_t ax, ay, az;
  mpu.getAcceleration(&ax, &ay, &az);
  float ax_g = ax / 16384.0;
  float ay_g = ay / 16384.0;
  float az_g = az / 16384.0;

  // write to SD
  SdFile myFile;
  myFile.open("unified.csv", O_WRITE | O_APPEND);
  myFile.print(millis());
  myFile.print(",");
  myFile.print(gps.location.lat(), 6);
  myFile.print(",");
  myFile.print(gps.location.lng(), 6);
  myFile.print(",");
  myFile.print(ax_g);
  myFile.print(",");
  myFile.print(ay_g);
  myFile.print(",");
  myFile.println(az_g);
  myFile.close();

  // print to serial monitor
  Serial.print("Lat: "); Serial.print(gps.location.lat(), 6);
  Serial.print(" Lng: "); Serial.print(gps.location.lng(), 6);
  Serial.print(" X: "); Serial.print(ax_g);
  Serial.print("g Y: "); Serial.print(ay_g);
  Serial.print("g Z: "); Serial.println(az_g);

  delay(500);
}