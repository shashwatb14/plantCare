#include <Arduino.h>
#include <Servo.h>
#include <DHT.h>

#define SERVO_PIN 9
#define DHT_PIN 8
#define DHT_TYPE DHT11
#define LIGHT_SENSOR_PIN A1
#define POWER_PIN  7
#define SIGNAL_PIN A5

Servo myservo;
DHT dht(DHT_PIN, DHT_TYPE);

const int wateringDuration = 2000; // 2 seconds
void setup() {
  Serial.begin(9600);
  myservo.attach(SERVO_PIN);
  dht.begin();
  delay(2000); // Wait for sensor to initialize
  pinMode(LIGHT_SENSOR_PIN, INPUT);
  pinMode(POWER_PIN, OUTPUT);
  digitalWrite(POWER_PIN, LOW);
}

void loop() {
  digitalWrite(POWER_PIN, LOW);  // turn the sensor ON
  int soilMoisture = analogRead(SIGNAL_PIN);
  int lightLevel = analogRead(LIGHT_SENSOR_PIN);
  float t = dht.readTemperature(); // Read temperature
  float h = dht.readHumidity();    // Read humidity

  Serial.print("TEMP: ");
  Serial.println(t);

  delay(2000);

  Serial.print("HUM: ");
  Serial.println(h);

  delay(2000);
  if (lightLevel < 400) {
    Serial.println("light low");
  }

  if (soilMoisture < 650) {
    Serial.println("WET");
  } else {
    Serial.println("DRY");
  }

  Serial.print("1 ");
  Serial.println(soilMoisture);
}

void waterPlant() {
  myservo.write(90); // Start watering
  delay(wateringDuration);
  myservo.write(0);  // Stop watering
  delay(1000);
}
