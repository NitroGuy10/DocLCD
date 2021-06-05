#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 20, 4);

/*
 * Pin connections:
 * 
 * RX -> Raspberry Pi TX
 * TX -> Raspberry Pi RX
 * GND -> Raspberry Pi Ground
 * 
 * 5V -> LCD VCC
 * GND -> LCD GND
 * A4 -> LCD SDA
 * A5 -> LCD SCL
 * 
 */

byte customChar[8] = {
  0b01010,
  0b01010,
  0b01010,
  0b00000,
  0b10001,
  0b10001,
  0b01110,
  0b00000
};

void setup() {
  lcd.init();
  // lcd.begin(20, 4);
  lcd.backlight();
  lcd.noBlink();
  lcd.cursor();
  lcd.home();
  lcd.print("Hello, LCD_Control!");
  lcd.createChar(0, customChar);
  lcd.setCursor(19, 0);
  lcd.write((byte) 0);

  Serial.begin(115200);
  
}

void loop() {
  if (Serial.available() > 0) {
    int incomingByte = Serial.read();
    if (incomingByte > 31)
    {
      lcd.print((char) incomingByte);
    }
    else if (incomingByte == 2)
    {
      int newX = Serial.parseInt();
      Serial.read(); // Ignore the separator byte (which should be char(3))
      int newY = Serial.parseInt();
      Serial.read(); // Ignore the separator byte (which should be char(0))
      lcd.setCursor(newX, newY);
    }
    else if (incomingByte == 1)
    {
      lcd.clear();
      lcd.home();
    }
    // Serial.println(Serial.read());
    
    //String incomingString = Serial.readStringUntil('\n');
    //Serial.println(incomingString);
    

  //Serial.println(Serial.readString());
  }
}
