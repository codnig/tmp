import RPi.GPIO as GPIO
import RPi_I2C_driver
import Adafruit_DHT
import time

GPIO.setmode(GPIO.BCM)

pumpPin = 20
fanPin = 21


GPIO.setup(pumpPin, GPIO.OUT)
GPIO.setup(fanPin, GPIO.OUT)

sensor = Adafruit_DHT.DHT11
pin = 4

times = 0

lcd = RPi_I2C_driver.lcd(0x27)


while True:
    global times
    times += 1
    h, t = Adafruit_DHT.read_retry(sensor, pin)
    msg = "TEMP{}C HUMI{}%".format(t, h)
    lcd.setCursor(0,1)
    lcd.print(msg)
    print(msg)
    
    if h is not None and t is not None :
        if times == 100 :
            if h < 70 :
                GPIO.output(pumpPin, GPIO.LOW)
                times = 0
                lcd.setCursor(0,0)
                lcd.print("PUMP START")
                lcd.setCursor(0,1)
                lcd.print(msg)
                print("PUMP START")
                time.sleep(3)
                GPIO.output(pumpPin, GPIO.HIGH)
                times += 1
            else : 
                GPIO.output(pumpPin, GPIO.HIGH)
                lcd.setCursor(0,0)
                lcd.print("PUMP STOP")
                lcd.setCursor(0,1)
                lcd.print(msg)
                print("PUMP STOP")
                time.sleep(2)
                times += 1

        if t > 29 :
            GPIO.output(fanPin, GPIO.LOW)
            lcd.setCursor(0,0)
            lcd.print("FAN START")
            lcd.setCursor(0,1)
            lcd.print(msg)
            print("FAN START")
            time.sleep(2)
            times += 1
        else :
            GPIO.output(fanPin, GPIO.HIGH)
            lcd.setCursor(0,0)
            lcd.print("FAN STOP")
            lcd.setCursor(0,1)
            lcd.print(msg)
            print("FAN STOP")
            time.sleep(2)
            times += 1
        
    else :
        lcd.print("ERROR")
        print("ERROR")
        time.sleep(1)

    time.sleep(1)
