from datetime import datetime

current_time = datetime.strftime(datetime.now(),"%H:%M") 

print(current_time)

mytime = "12:19"

if current_time == mytime:
    print ("Time match.")
