#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

// Definir el patrón de un corazón como un arreglo de bytes
byte corazon[8] = {
  B00000,
  B01010,
  B11111,
  B11111,
  B01110,
  B00100,
  B00000,
};

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

void setup() {
  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("UNIVERSIDAD EIA");
  lcd.setCursor(0, 1);
  lcd.print("QUADRUPED ROBOT");

  // Crear el carácter personalizado en la posición 1 (índice 0)
  lcd.createChar(1, corazon);
  lcd.createChar(2, QR);
  lcd.createChar(3, EIA);
  lcd.setCursor(15, 0);
  lcd.write(byte(3));
  lcd.setCursor(15, 1);
  lcd.write(byte(2));
}

void loop() {
  lcd.display();
  
  
}

