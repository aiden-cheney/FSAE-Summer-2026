#include <Wire.h>
#include <MPU6050.h>

// create MPU6050 object
MPU6050 mpu;

void setup() {
  // start serial monitor
  Serial.begin(9600);
  
  // start I2C communication
  Wire.begin();
  
  // initialize MPU6050
  mpu.initialize();

  // set accelerometer range to +/- 2g
  mpu.setFullScaleAccelRange(MPU6050_ACCEL_FS_2);
  
  // check if its connected
  if (mpu.testConnection()) {
    Serial.println("MPU6050 connected!");
  } else {
    Serial.println("MPU6050 connection failed!");
  }
}

void loop() {
  // variables to store acceleration values
  int16_t ax, ay, az;
  
  // read raw acceleration values from sensor
  mpu.getAcceleration(&ax, &ay, &az);
  
  // convert raw values to g-forces by dividing by 16384
  float ax_g = ax / 16384.0;
  float ay_g = ay / 16384.0;
  float az_g = az / 16384.0;
  
  // print converted g-force values
  Serial.print("X: "); Serial.print(ax_g);
  Serial.print("g  Y: "); Serial.print(ay_g);
  Serial.print("g  Z: "); Serial.print(az_g);
  Serial.println("g");
  
  // wait 2000ms between readings
  delay(2000);
}
