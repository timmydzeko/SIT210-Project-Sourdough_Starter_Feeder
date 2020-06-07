# Library for 28BYJ-48 stepper motor and ULN2003 driver control
import RPi.GPIO as GPIO
import time

def stepperLeft():
    GPIO.setmode(GPIO.BCM)
    control_pins = [2,3,4,14]
    for pin in control_pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.setwarnings(False)
        GPIO.output(pin, 0)
    halfstep_seq_fwd = [
        [1,0,0,0],
        [1,1,0,0],
        [0,1,0,0],
        [0,1,1,0],
        [0,0,1,0],
        [0,0,1,1],
        [0,0,0,1],
        [1,0,0,1]
    ]
    for i in range(5400):
        for halfstep in range(8):
            for pin in range(4):
                GPIO.output(control_pins[pin], halfstep_seq_fwd[halfstep][pin])
                time.sleep(0.0003)
    time.sleep(5)
    halfstep_seq_rev = [
      [1,0,0,1],
      [0,0,0,1],
      [0,0,1,1],
      [0,0,1,0],
      [0,1,1,0],
      [0,1,0,0],
      [1,1,0,0],
      [1,0,0,0]
    ]
    for i in range(5400):
        for halfstep in range(8):
            for pin in range(4):
                GPIO.output(control_pins[pin], halfstep_seq_rev[halfstep][pin])
                time.sleep(0.0003)
    time.sleep(2)
    for pin in range(4):
        GPIO.output(control_pins[pin], 0) #sets all pins to 0V to conserve power
    GPIO.cleanup()
    
def stepperRight():
    GPIO.setmode(GPIO.BCM)
    control_pins = [19,26,20,21]
    for pin in control_pins:
        GPIO.setwarnings(False)
        GPIO.setup(pin, GPIO.OUT)
        
        GPIO.output(pin, 0)
    halfstep_seq_rev = [
      [1,0,0,1],
      [0,0,0,1],
      [0,0,1,1],
      [0,0,1,0],
      [0,1,1,0],
      [0,1,0,0],
      [1,1,0,0],
      [1,0,0,0]
    ]
    for i in range(5400):
        for halfstep in range(8):
            for pin in range(4):
                GPIO.output(control_pins[pin], halfstep_seq_rev[halfstep][pin])
                time.sleep(0.0003)
    time.sleep(5)
    halfstep_seq_fwd = [
        [1,0,0,0],
        [1,1,0,0],
        [0,1,0,0],
        [0,1,1,0],
        [0,0,1,0],
        [0,0,1,1],
        [0,0,0,1],
        [1,0,0,1]
    ]
    for i in range(5400):
        for halfstep in range(8):
            for pin in range(4):
                GPIO.output(control_pins[pin], halfstep_seq_fwd[halfstep][pin])
                time.sleep(0.0003)
    GPIO.cleanup()
