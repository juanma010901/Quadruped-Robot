#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("UNIVERSIDAD EIA");
  lcd.setCursor(0, 1);
  lcd.print("QUADRUPED ROBOT");

  // Crear el carácter personalizado en la posición 1 (índice 0)

}

void loop() {
  lcd.display();
  
  
}

