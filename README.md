# DocLCD
A lightweight "word processor" for 20x4 character LCDs with a 4-pin I2C controller

I used a Raspberry Pi 2 and an Arduino Uno in my design.
DocLCD may break or behave differently if you have different models.

## Physical Setup

```
/*
 * Pin connections:
 * 
 * Ardunio RX -> Raspberry Pi TX
 * Arduino TX -> Raspberry Pi RX
 * Arduino GND -> Raspberry Pi Ground
 * 
 * Arduino 5V -> LCD VCC
 * Arduino GND -> LCD GND
 * Arduino A4 -> LCD SDA
 * Arduino A5 -> LCD SCL
 * 
 */
```

## Arduino Setup

Load LCD_Control.ino onto your Arduino.
It uses the library [LiquidCrystal_I2C](https://www.arduino.cc/reference/en/libraries/liquidcrystal-i2c/).

Note that if your Arduino's TX and RX are connected to your Raspberry Pi while loading programs, your Arduino may behave oddly and the program may not be loaded successfully.
Disconnect TX and RX while loading programs to avoid this.

## Raspberry Pi Setup

main[]().py is the script you will run on your Raspberry Pi.
It accepts keyboard input and allows you type characters and traverse around the LCD screen.

Before running, two things must be done. 1) The Python libraries [PySerial](https://github.com/pyserial/pyserial/) and [Pygame](https://www.pygame.org/) must be installed and 2) the serial port of your Raspberry Pi must be enabled.
There are a couple of ways to do this and they may vary depending on the model of Raspberry Pi. I recommend searching online how to do this.
