#include <Wire.h>
#include <MPU6050.h>
#include <SdFat.h>
#include <SPI.h>

// create MPU6050 and SD objects
MPU6050 mpu;
SdFat SD;

// SD card chip select pin
#define CS_PIN 10

void setup() {
  Serial.begin(9600);
  Wire.begin();
  
  // initialize MPU6050
  mpu.initialize();
  mpu.setFullScaleAccelRange(MPU6050_ACCEL_FS_2);
  Serial.println("MPU6050 ready!");

  // initialize SD card
  if (!SD.begin(CS_PIN)) {
    Serial.println("SD card failed!");
    return;
  }
  Serial.println("SD card ready!");

  // create CSV file with headers
  SdFile myFile;
  myFile.open("accel.csv", O_WRITE | O_CREAT);
  myFile.println("time,x_g,y_g,z_g");
  myFile.close();
}

void loop() {
  int16_t ax, ay, az;
  mpu.getAcceleration(&ax, &ay, &az);

  // convert to g-forces
  float ax_g = ax / 16384.0;
  float ay_g = ay / 16384.0;
  float az_g = az / 16384.0;

  // write to SD card
  SdFile myFile;
  myFile.open("accel.csv", O_WRITE | O_APPEND);
  myFile.print(millis());
  myFile.print(",");
  myFile.print(ax_g);
  myFile.print(",");
  myFile.print(ay_g);
  myFile.print(",");
  myFile.println(az_g);
  myFile.close();

  // print to serial monitor so we can see it working
  Serial.print("X: "); Serial.print(ax_g);
  Serial.print("g  Y: "); Serial.print(ay_g);
  Serial.print("g  Z: "); Serial.print(az_g);
  Serial.println("g");

  // log every 500ms
  delay(500);
}