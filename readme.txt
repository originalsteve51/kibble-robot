1. Start the two programs feeder.py and distance.py so they run in the background, unattended, and append their log files.

2. Copy the feeder.out file to the machine where the web server runs. A shell script named copy-status.sh is used to do this using scp (secure copy) to the fixed ip address of the web server machine.


3. Do these automatically using crontab

crontab -l shows

pi@orb-pi:~/mycode/stepper/kibble-robot $ crontab -l

*/5 * * * * cd /home/pi/mycode/stepper/kibble-robot; ./copy-status.sh  
@reboot sleep 30; /usr/bin/python3 -u ~/mycode/stepper/kibble-robot/distance.py >> ~/mycode/stepper/kibble-robot/distance.out &
@reboot sleep 30; /usr/bin/python3 -u ~/mycode/stepper/kibble-robot/feeder.py >> ~/mycode/stepper/kibble-robot/feeder.out &

Note that the first crontab line runs copy-status.sh every five minutes. The other lines run the distance and feeder python programs each time the machine is rebooted.

