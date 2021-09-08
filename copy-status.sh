#!/bin/bash
tail -100 ./feeder.out > ./feedtail.out
sshpass -p 'pi-pass' scp ./feedtail.out pi@192.168.1.30:/home/pi/mycode/webapp 

