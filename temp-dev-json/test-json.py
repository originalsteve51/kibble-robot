import json
from datetime import datetime

"""
cd = datetime.datetime.now()
current_date = cd.strftime("%m/%d/%Y")
current_time = cd.strftime("%H:%M")
"""

current_date = datetime.strftime(datetime.now(),"%m/%d/%Y")
current_time = datetime.strftime(datetime.now(),"%H:%M") 

run_data = dict()
run_data[current_date] = dict()
run_data[current_date]['start_feed'] = current_time
run_data[current_date]['start_weight'] = .023
run_data[current_date]['end_weight'] = .102
run_data[current_date]['stable_weight'] = .107
run_data[current_date]['details'] = [.023, .023, .023, .037, .054, .075, .102]

j_str = json.dumps(run_data)

print(j_str)

new_run_data = json.loads(j_str)

print(new_run_data[current_date]['details'])