import board
import busio
import adafruit_character_lcd.character_lcd_i2c as characterlcd
i2c = busio.I2C(board.SCL, board.SDA)
lcd_columns = 16
lcd_rows = 2
lcd = characterlcd.Character_LCD_I2C(i2c, lcd_columns, lcd_rows, address = 0x27)
lcd.clear()
lcd.message = "Hello, LCD!"
lcd.cursor_position(0, 1)
