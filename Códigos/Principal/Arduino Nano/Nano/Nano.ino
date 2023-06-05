#include <ArduinoJson.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h> 

LiquidCrystal_I2C lcd(0x27,16,2);

byte QR[8] = {
  B00000,
  B00000,
  B11111,
  B11111,
  B01001,
  B10010,
  B01001,
  B00000
};

byte EIA[8] = {
  B11111,
  B01110,
  B00100,
  B11011,
  B11011,
  B00100,
  B00100,
  B00000
};

int N1 = A0;
int N2 = A1;
int N3 = A2;
int N4 = A3;
int N5 = A6;
int N6 = A7;

int M1 = 0;
int M3 = 0;
int M5 = 0;
int M7 = 0;
int M2 = 0;
int M4 = 0;

void setup() {
  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("UNIVERSIDAD EIA");
  lcd.setCursor(0, 1);
  lcd.print("QUADRUPED ROBOT");

  // Crear el carácter personalizado en la posición 1 (índice 0)
  lcd.createChar(1, QR);
  lcd.createChar(2, EIA);
  lcd.setCursor(15, 0);
  lcd.write(byte(2));
  lcd.setCursor(15, 1);
  lcd.write(byte(1));

  pinMode(N1, INPUT);
  pinMode(N2, INPUT);
  pinMode(N3, INPUT);
  pinMode(N4, INPUT);
  pinMode(N5, INPUT);
  pinMode(N6, INPUT);

  Serial.begin(9600);
}

void loop() {
  lcd.display();

  M1 = analogRead(N1);
  M3 = analogRead(N2);
  M5 = analogRead(N3);
  M7 = analogRead(N4);
  M2 = analogRead(N5);
  M4 = analogRead(N6);

  // Crear el documento JSON
  DynamicJsonDocument doc(128);

  // Agregar datos al JSON
  doc["A11"] = M1;
  doc["A21"] = M3;
  doc["A31"] = M5;
  doc["A41"] = M7;
  doc["A12"] = M2;
  doc["A22"] = M4;

  // Serializar el JSON en un búfer
  char buffer[128];
  serializeJson(doc, buffer);

  // Enviar el JSON a través del puerto serial
  Serial.println(buffer);

  delay(500);
}
