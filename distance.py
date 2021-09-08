import RPi.GPIO as GPIO
import time
import apa
from datetime import datetime
from sensor import *
import threading
import mqtt_sub


numleds = 8   
brightness_presets = [0,5,15,31]
brightness_idx = len(brightness_presets)-1
lights_on = False

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
PIN_TRIGGER = 20
PIN_ECHO = 19

# Turn all leds on with a specified brightness
# brightness value. 0 = OFF, 31 = FULL
def all_on(brightness, r=255, g=255, b=255):
    some_on(brightness)
    
def some_on(brightness, r=255, g=255, b=255, num_on=8):
	# set all LEDs to full white with specified brightness
	for led in range(8):
		led_strip.led_set(led, 0, 0, 0, 0)
	for led in range(num_on):
		led_strip.led_set(led, brightness, b, g, r)

	# Let there be light!
	led_strip.write_leds()
    

def toggle_on_off():
	global lights_on
	if lights_on:
		led_strip.reset_leds()
		lights_on = False
	else:
		all_on(brightness_presets[brightness_idx])
		lights_on = True

def change_brightness():
	global brightness_idx
	if lights_on:
		if brightness_idx < len(brightness_presets)-1:
			brightness_idx += 1
		else:
			brightness_idx = 0
		all_on(brightness_presets[brightness_idx])

def msg_listener():
    print('listener thread started')
    while True:
        msg = mqtt_sub.listen_for_msgs()
        #print('received: ', msg)
        if msg == 'pan-home':
            toggle_on_off()
        

if __name__ == '__main__':

    # initialize the LED strip. Receive back led_strip, which is used to control the LEDs
    led_strip = apa.Apa(numleds) 
    led_strip.flush_leds()

    # Start listening for messages, subscribing to a topic specified in mqtt_sub
    x = threading.Thread(target=mqtt_sub.run)
    x.start()
    
    y = threading.Thread(target=msg_listener)
    y.start()
    
    
    try:
    
        cat_sensor = Sensor('Cat', PIN_TRIGGER, PIN_ECHO)
    
        while True:
                
            distance = cat_sensor.measure()
    
    
            if distance < 60.0: 
                some_on(255,255,255,255,8)
                current_time = datetime.strftime(datetime.now(),"%H:%M") 
                current_date = datetime.strftime(datetime.now(),"%m/%d/%Y")
                print('cat sensor triggered: ', current_date, ' at ', current_time)
                time.sleep(150)
            else:
                if not lights_on:
                    some_on(0,0,0,0,8)
                


            # print ("Distance:",distance,"cm")
            time.sleep(0.5)    
    finally:
        GPIO.cleanup()