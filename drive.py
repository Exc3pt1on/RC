
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(24,GPIO.OUT)
servo1 = GPIO.PWM(24,50)
servo1.start(0)
print ("Waiting for 2 seconds")
time.sleep(2)

duty = 9

print(duty)
servo1.ChangeDutyCycle(9)

time.sleep(2)
print("7")
servo1.ChangeDutyCycle(7)

time.sleep(2)
while True:
    speed = input("Input speed for 2 seconds: (x to stop)")
    if speed == "x":
        break
    else:
        print(speed)
        servo1.ChangeDutyCycle(speed)
        time.sleep(2)
        servo1.ChangeDutyCycle(7)

time.sleep(2)
print("7")
servo1.ChangeDutyCycle(7)

servo1.stop()
GPIO.cleanup()
