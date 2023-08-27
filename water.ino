#include <Arduino.h>
#include <Servo.h>


#define SERVO_PIN 9
#define LIGHT_SENSOR_PIN A1
#define POWER_PIN 7
#define SIGNAL_PIN A5


Servo myservo;


const int wateringDuration = 2000; // 2 seconds


void setup() {
  Serial.begin(9600);
  myservo.attach(SERVO_PIN);
  pinMode(LIGHT_SENSOR_PIN, INPUT);
  pinMode(POWER_PIN, OUTPUT); // configure D7 pin as an OUTPUT
  digitalWrite(POWER_PIN, LOW); // turn the sensor OFF
}


void loop() {
  digitalWrite(POWER_PIN, LOW); // turn the sensor ON
  int soilMoisture = analogRead(SIGNAL_PIN); // read the analog value from sensor
  int lightLevel = analogRead(LIGHT_SENSOR_PIN);
  String light_condition = "";
  String soil_condition = "";

  if (lightLevel < 400) {
    waterPlant();
    light_condition = "light low";
  } else {
    light_condition = "light okay";
  }

  if (soilMoisture < 650) {
    waterPlant();
    soil_condition = "DRY";
  } else {
    soil_condition = "WET";
  }

  // Send data as a comma-separated string
  String sensor_data = light_condition + "," + soil_condition;
  Serial.println(sensor_data);

  delay(5000);  // Delay for a second
}



void waterPlant() {
  myservo.write(90); // Start watering
  delay(wateringDuration);
  myservo.write(0); // Stop watering
  delay(1000);
}
