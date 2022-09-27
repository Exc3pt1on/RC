import time
import RPi.GPIO as GPIO
import threading
from flask import Flask, render_template, request
app = Flask(__name__)

program_run = False

try:
    def dist():

        #LEFT
        error_left = False
        GPIO.output(TRIG_L, 1)
        time.sleep(0.00001)
        GPIO.output(TRIG_L, 0)

        fail_test = time.time()

        while GPIO.input(ECHO_L) == 0:
            now = time.time()
            if fail_test - now > 1:
                error_left = True
                print('Error sensor left')
                break
            pass

        if error_left == False:
            start = time.time()

            while GPIO.input(ECHO_L) == 1:
                pass
            stop = time.time()
            distance = (stop - start) * 17000
            left = distance
        else:
            left = 50

        #CENTER
        error_center = False
        GPIO.output(TRIG_S, 1)
        time.sleep(0.00001)
        GPIO.output(TRIG_S, 0)

        fail_test = time.time()

        while GPIO.input(ECHO_S) == 0:
            now = time.time()
            if fail_test - now > 1:
                error_center = True
                print('Error sensor center')
                break
            pass

        if error_center == False:
            start = time.time()

            while GPIO.input(ECHO_S) == 1:
                pass
            stop = time.time()

            distance = (stop - start) * 17000
            center = distance
        else:
            center = 0

        #RIGTH
        error_right = False
        GPIO.output(TRIG_R, 1)
        time.sleep(0.00001)
        GPIO.output(TRIG_R, 0)

        fail_test = time.time()

        while GPIO.input(ECHO_R) == 0:
            now = time.time()
            if fail_test - now > 1:
                error_right = True
                print('Error sensor right')
                break
            pass

        if error_right == False:
            start = time.time()

            while GPIO.input(ECHO_R) == 1:
                pass
            stop = time.time()

            distance = (stop - start) * 17000
            right = distance
        else:
            right = 50

        return left, center, right
    
    
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
    print ("Starting system")
    time.sleep(2)

    gass.ChangeDutyCycle(9)
    time.sleep(2)
    gass.ChangeDutyCycle(7)
    turn.ChangeDutyCycle(7)

    time.sleep(2)

    def main():
        global program_run
        program_run = True
        
        speed = 7.5

        while program_run:

            left,center,right = dist()

            #Gass
            if center > 50:
                gass.ChangeDutyCycle(speed)
            elif center == 0:
                gass.ChangeDutyCycle(7)
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
                # gass.ChangeDutyCycle(6)
                # time.sleep(0.5)


            #Steering
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

        #After ended run
        gass.ChangeDutyCycle(7)
        turn.ChangeDutyCycle(7)





    @app.route("/")
    def index():
        return render_template('index.html')
    @app.route("/<deviceName>/")
    def action(deviceName):
        if deviceName == 'start':
            #run python program
            main_program = threading.Thread(target=main, daemon=True)  #mayby implement thread.is_alive() and not allow multiple to run simultaneously
            main_program.start()
            print('main finished')
        elif deviceName == 'stop':
            #stop python program
            global program_run
            program_run = False
            print('stop')
        return render_template('index.html')
    if __name__ == "__main__":
        app.run(host='0.0.0.0', port=80, debug=True)

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
    print('done')