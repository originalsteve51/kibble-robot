#!/bin/bash
#tail -100 ./status.json > ./feedtail.out
sshpass -p 'pi-pass' scp ./status.json pi@192.168.1.30:/home/pi/mycode/webapp 

