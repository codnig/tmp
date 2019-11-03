import RPi.GPIO as GPIO
import RPi_I2C_driver
import Adafruit_DHT
import time

GPIO.setmode(GPIO.BCM)
#핀 선언
pumpPin = 21
fanPin = 20

#핀 설정
GPIO.setup(pumpPin, GPIO.OUT)
GPIO.setup(fanPin, GPIO.OUT)

sensor = Adafruit_DHT.DHT11
pin = 4

times = 0

lcd = RPi_I2C_driver.lcd(0x27)


while True:
    h, t = Adafruit_DHT.read_retry(sensor, pin)
    global times
    times += 1
    if h is not None and t is not None :

        if times == 120 and h < 70 :
            GPIO.output(pumpPin, GPIO.LOW)
            times = 0
            lcd.print("PUMP START")
            time.sleep(2)
            times += 1
        else : 
            GPIO.output(pumpPin, GPIO.HIGH)
            lcd.print=("PUMP STOP")
            time.sleep(2)
            times += 1

        if t > 29 :
            GPIO.output(fanPin, GPIO.LOW)
            lcd.print("FAN START")
            time.sleep(2)
            times += 1
        else :
            GPIO.output(fanPin, GPIO.HIGH)
            lcd.print("FAN STOP")
            time.sleep(2)
            times += 1

    else :
        lcd.print("ERROR")
        time.sleep(1)
    
    msg = "TEMP : {}C HUMI : {}\%".format(t, h)

    lcd.print(msg)

    time.sleep(1) #1초마다 반복
