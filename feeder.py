#!/usr/bin/python
import time
import RPi.GPIO as GPIO
from hx711 import HX711
import sys

from datetime import datetime

import threading
import mqtt_sub

def initialize_feeder(motor_pin_list, scale_pin_1, scale_pin_2):
    
    # Use BCM GPIO references
    # instead of physical pin numbers
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Set all pins as output
    for pin in motor_pin_list:
        # print "Setup pins"
        GPIO.setup(pin,GPIO.OUT)
        GPIO.output(pin, False)
    
    reference_unit = 1
    
    # The last line in the log file is always the most recent weight recorded
    # by the system. This value is read at start-up to determine the amount of
    # food present and to establish the scale offset.
    # log_file_name = "feeder.out"
    
    # print("Scale offset:\n", get_scale_offset(log_file_name)) 
     
    # Define some settings
    step_counter = 0
    wait_time = 0.02

    # Obtain the weighing component (strain gauge and a/d converter)
    hx = HX711(scale_pin_1, scale_pin_2)
    
    # Initialize the strain gauge and its a/d converter    
    # The first parameter is the order in which the bytes are used to build the "long" value.
    # The second paramter is the order of the bits inside each byte.
    # According to the HX711 Datasheet, the second parameter is MSB so you shouldn't need to modify it.
    hx.set_reading_format("MSB", "MSB")
    hx.set_reference_unit(reference_unit)
    hx.reset()
    hx.tare()
    #print("Tare done! Scale is ready.")
    
    return hx

def get_weight(hx):
    val = hx.get_weight(5)/916000
    hx.power_down()
    hx.power_up()
    return val

def run_feed_motor(hx, direction='cw'):
    # global scale_offset
     
    wait_time = 0.02
    
    if direction == 'cw':
        directionFlag = False
    elif direction == 'ccw':
        directionFlag = True
    else:
        print ('Weight: ', format(get_weight(hx), '.3f') )
        return
        
    cycle_counter = 1
    GPIO.output(direction_pin, directionFlag)
    val = get_weight(hx)
    # Only run motor if weight is under 0.25
    while True and val < 0.25:
        if cycle_counter % 3 == 0:
            print ('Direction: ',direction)
            time.sleep(1)
            val = get_weight(hx)
            print('Weight: ',format(val, '.3f'))
            break    
        for step in range(15) :
            GPIO.output(step_pin, True)
            time.sleep(wait_time*3)
            GPIO.output(step_pin, False)
        cycle_counter += 1
    return val

def auto_feed(feed_times, direction_pin, step_pin, hx, feed_the_cat=False):
    # global scale_offset
    wait_time = 0.02
    while True:
        current_date = datetime.strftime(datetime.now(),"%m/%d/%Y")
        current_time = datetime.strftime(datetime.now(),"%H:%M") 
        if not feed_the_cat:
            for a_time in feed_times:
                if current_time == a_time:
                    feed_the_cat = True
                    break

            current_minute = datetime.strftime(datetime.now(),"%M")
            # Every hour on the half-hour write the current weight to the std out
            # file. This allows the file to be read so you can see the food consumption
            # each hour.
            if current_minute == "30":
                val = get_weight(hx)
                print(current_time, ":\n",format(val, '.3f'))
            time.sleep(55)
        else:
            step_counter = 0
            val = get_weight(hx)
            print(current_date)
            print("Checked weight of food at ",current_time,": ",format(val, '.3f'))
            
            # Run the feeder up to 40 bursts to 'fill' the bowl
            while val < 0.1 and step_counter < 400:
                GPIO.output(step_pin, True)
                time.sleep(wait_time*3)
                GPIO.output(step_pin, False)
                if step_counter % 10 == 0:
                    val = get_weight(hx)
                    # Write the weight every 10 steps to the std out file
                    # The log will show an increase, hopefully, every 10 steps of the feed motor
                    print(format(val, '.3f'))
                step_counter += 1
            feed_the_cat = False
            time.sleep(60)
            val = get_weight(hx)
            print("Stable weight one minute after feed cycle:\n",format(val, '.3f'))

def msg_listener(hx):
    # print('listener thread started')
    while True:
        msg = mqtt_sub.listen_for_msgs()
        current_time = datetime.strftime(datetime.now(),"%H:%M") 
        #print(current_time, ' received: ', msg)
        if msg == 'pan-left':
            run_feed_motor(hx, 'cw')
        elif msg == 'pan-right':
            run_feed_motor(hx, 'ccw')


def clean_up(motor_pin_list):
    for pin in motor_pin_list:
        GPIO.output(pin, False)
    GPIO.cleanup()
    # print("Bye!")
    sys.exit()

if __name__ == '__main__':
    
    feed_time_list = ["07:00","12:00","19:00", "23:00"]
    
    # Motor control pins
    direction_pin = 25
    step_pin = 24
    motor_pin_list = [direction_pin, step_pin] 

    # Scale (for weighing food) control pins
    scale_pin_1 = 5
    scale_pin_2 = 6
    
    try:
        hx = initialize_feeder(motor_pin_list, scale_pin_1, scale_pin_2)
        
        x = threading.Thread(target=mqtt_sub.run)
        x.start()
        
        y = threading.Thread(target=msg_listener, args=(hx,))
        y.start()

        auto_feed(feed_time_list, direction_pin, step_pin, hx, False)
    finally:
        clean_up(motor_pin_list)