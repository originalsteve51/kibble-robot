#!/usr/bin/python
import time
import RPi.GPIO as GPIO
from hx711 import HX711

import threading
import mqtt_sub

direction_pin = 25
step_pin = 24


def get_weight():
    val = hx.get_weight(5)/916000
    
    hx.power_down()
    hx.power_up()
    return val

def run_feed_motor(direction='cw'): 
    print('run_feed_motor: ', direction)
    
    StepCounter = 0
    WaitTime = 0.02
    
    if direction == 'cw':
        directionFlag = False
    elif direction == 'ccw':
        directionFlag = True
    else:
        print ('Weight since last tare: ', format(get_weight(), '.3f') )
        return
        
        
    cycle_counter = 1
    GPIO.output(direction_pin, directionFlag)
    while True:
        if cycle_counter % 3 == 0:
            print ('Direction flag: ',directionFlag)
            time.sleep(1)
            val = get_weight()
            print('Weight since last tare: ',format(val, '.3f'))
            break    
        for step in range(15) :
            GPIO.output(step_pin, True)
            time.sleep(WaitTime*3)
            GPIO.output(step_pin, False)
        cycle_counter += 1
    return val

if __name__ == '__main__':
    
    # Use BCM GPIO references
    # instead of physical pin numbers
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    
    # Start listening for messages, subscribing to a topic specified in mqtt_sub
    x = threading.Thread(target=mqtt_sub.run)
    x.start()
    
    
    # Set up the scale to weigh the food
    reference_unit = 1
    hx = HX711(5, 6)
    hx.set_reading_format("MSB", "MSB")
    
    hx.set_reference_unit(reference_unit)
    
    hx.reset()
    
    hx.tare()
    
    print("Tare done! Add weight now...")
    
     
    
    pins = [direction_pin, step_pin] 
    # Set all pins as output
    for pin in pins:
        # print "Setup pins"
        GPIO.setup(pin,GPIO.OUT)
        GPIO.output(pin, False)
    
    try:
        while True:
            msg = mqtt_sub.listen_for_msgs()
    
            if msg == 'pan-left':
                run_feed_motor()
                
            if msg == 'pan-home':
                run_feed_motor('light')
    
            elif msg == 'pan-right':
                run_feed_motor('ccw')
                        
    finally:
        # After a keyboard interrupt or anything else that shuts things down,
        # turn off the LED strand
        print("BYE!")
