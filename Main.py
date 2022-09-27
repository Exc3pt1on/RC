import RPi.GPIO as GPIO
import time

def dist():

    #LEFT
    GPIO.output(TRIG_L, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG_L, 0)

    while GPIO.input(ECHO_L) == 0:
        pass

    start = time.time()

    while GPIO.input(ECHO_L) == 1:
        pass
    stop = time.time()
    distance = (stop - start) * 17000
    left = distance

    #CENTER
    GPIO.output(TRIG_S, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG_S, 0)

    while GPIO.input(ECHO_S) == 0:
        pass

    start = time.time()

    while GPIO.input(ECHO_S) == 1:
        pass
    stop = time.time()

    distance = (stop - start) * 17000
    center = distance

    #RIGTH
    GPIO.output(TRIG_R, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG_R, 0)

    while GPIO.input(ECHO_R) == 0:
        pass

    start = time.time()

    while GPIO.input(ECHO_R) == 1:
        pass
    stop = time.time()

    distance = (stop - start) * 17000
    right = distance
    
    return left, center, right

try:

    GPIO.setmode(GPIO.BOARD)

    TRIG_L = 3
    TRIG_S = 5
    TRIG_R = 7

    ECHO_L = 11
    ECHO_S = 13
    ECHO_R = 15

    GPIO.setup(TRIG_L, GPIO.OUT)
    GPIO.output(TRIG_L, 0)

    GPIO.setup(TRIG_S, GPIO.OUT)
    GPIO.output(TRIG_S, 0)

    GPIO.setup(TRIG_R, GPIO.OUT)
    GPIO.output(TRIG_R, 0)

    GPIO.setup(ECHO_L, GPIO.IN)
    GPIO.setup(ECHO_S, GPIO.IN)
    GPIO.setup(ECHO_R, GPIO.IN)

    time.sleep(0.1)

    GPIO.setup(22,GPIO.OUT)
    turn = GPIO.PWM(22,50)
    turn.start(0)
    time.sleep(2)

    GPIO.setup(24,GPIO.OUT)
    gass = GPIO.PWM(24,50)
    gass.start(0)
    print ("Startup 4 sek")
    time.sleep(2)

    duty = 9

    print(duty)
    gass.ChangeDutyCycle(9)

    time.sleep(2)

    print("7")
    gass.ChangeDutyCycle(7)
    turn.ChangeDutyCycle(7)

    time.sleep(2)

    while True:

        left,center,right = dist()
        if center > 50:
            gass.ChangeDutyCycle(7.5)
        else:
            gass.ChangeDutyCycle(7)
            time.sleep(1)
            if left > right:
                turn.ChangeDutyCycle(5)
            else:
                turn.ChangeDutyCycle(9)
            time.sleep(0.5)
            gass.ChangeDutyCycle(5)
            time.sleep(0.2)
            gass.ChangeDutyCycle(7)
            time.sleep(0.2)
            gass.ChangeDutyCycle(6)
            time.sleep(0.5)

        if center < 200:
            if (right - 10) > left:
                turn.ChangeDutyCycle(5)
            elif (left - 10) > right:
                turn.ChangeDutyCycle(9)
            else:
                turn.ChangeDutyCycle(7)
        else:
            if (left < 30) or (right < 30):
                if left < right:
                    turn.ChangeDutyCycle(5)
                else:
                    turn.ChangeDutyCycle(9)
            else:
                turn.ChangeDutyCycle(7)

    

except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
   print("Keyboard interrupt")

except:
   print("some error") 

finally:
   print("clean up") 
   turn.ChangeDutyCycle(7)
   time.sleep(0.2)
   turn.stop()
   gass.stop()
   GPIO.cleanup() # cleanup all GPIO 
