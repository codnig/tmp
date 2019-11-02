import RPi.GPIO as GPIO
import Adafruit_CharLCD as LCD
import Adafruit_DHT
import time

GPIO.setmode(GPIO.BCM)
#핀 선언
pumpPin = 21
ledPin = 20
fanPin = 16

lcdRs = 25
lcdEn = 24
lcdD4 = 23
lcdD5 = 17
lcdD6 = 18
lcdD7 = 22
lcdBacklight = 2

lcdColumns = 16
lcdRows = 2

lcd = LCD.Adafruit_CharLCD(lcdRs, lcdEn, lcdD4, lcdD5, lcdD6, lcdD7, lcdColumns, lcdRows, lcdBacklight)
#핀 설정
GPIO.setup(pumpPin, GPIO.OUT)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(fanPin, GPIO.OUT)
#파이어 베이스의 data 데이터 받아오기 (센서 값)

sensor = Adafruit_DHT.DHT11
pin = 4

times = 0

while True:
    h, t = Adafruit_DHT.read_retry(sensor, pin)
    global times
    times += 1
    if h is not None and t is not None :
        lcd.message(h)

        if times == 600 and h > 20 :
            GPIO.output(pumpPin, GPIO.HIGH)
            times = 0
            lcd.message=("PUMP START")
        else : 
            GPIO.output(pumpPin, GPIO.LOW)
            lcd.message=("PUMP STOP")

        if t > 29 :
            GPIO.output(fanPin, GPIO.HIGH)
            lcd.message("FAN START")
        else :
            GPIO.output(fanPin, GPIO.LOW)
            lcd.message("FAN STOP")

    else :
        lcd.message("ERROR")
    
    msg = "TEMP : {}C HUMI : {}\%".format(t, h)

    lcd.message(msg)

    lcd.clear()
    
    time.sleep(1) #1초마다 반복


"""
라즈베리파이에서 온습도 센서를 통해 테이터를 입력받고,
16*2 lcd에 온도와 습도를 출력한 다음 그 데이터를
통해 온도와 습도가 일정 수준보다 낮을 시 릴레이를
작동시켜 모터팬이나 펌프를 구동시키는 시스템을 파이썬을
통해 구현하는 시스템도 가능할까요?
"""