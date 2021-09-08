import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)


class Sensor:
    def __init__(self, sensor_name, gpio_trigger_pin, gpio_echo_pin):
        self.name = sensor_name
        self.trigger_pin = gpio_trigger_pin
        self.echo_pin = gpio_echo_pin

        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        GPIO.output(self.trigger_pin, GPIO.LOW)
    
        #print ("Waiting for sensor to settle")
        time.sleep(2)
        print (self.name, ": Sensor ready")

    def measure(self):
        while True:
            try:
                GPIO.output(self.trigger_pin, GPIO.HIGH)
                
                time.sleep(0.00001)
                
                GPIO.output(self.trigger_pin, GPIO.LOW)
                  
                hang_counter = 0  
                hung_flag = False
                while GPIO.input(self.echo_pin)==0:
                    hang_counter += 1
                    if hang_counter > 10000:
                        hung_flag = True
                        break
                    pulse_start_time = time.time()
                if hung_flag:
                    print('Sensor hang loop 1')
                    continue
                hang_counter = 0    
                while GPIO.input(self.echo_pin)==1:
                    # """
                    hang_counter += 1
                    if hang_counter > 30000:
                        hung_flag = True
                        break
                    # """
                    pulse_end_time = time.time()
                if hung_flag:
                    print('Sensor hang loop 2')
                    continue    
                pulse_duration = pulse_end_time - pulse_start_time
                break
            except NameError:
                print('caught NameError exception')
                continue
            
        distance = round(pulse_duration * 17150, 2)
        return distance
        
if __name__ =='__main__':
    cat_sensor = Sensor('Cat', 20, 19)
    
    print("Measure: ", cat_sensor.measure())
        
        

    

