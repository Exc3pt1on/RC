import RPi.GPIO as GPIO
import time



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

    print("Starting Measurement")

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
    print("Distance left:", distance)

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
    print("Distance center:", distance)

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
    print("Distance right:", distance)
                
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
   print("Keyboard interrupt")

except:
   print("some error") 

finally:
   print("clean up") 
   GPIO.cleanup() # cleanup all GPIO 