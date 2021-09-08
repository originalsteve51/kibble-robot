import json
import datetime

run_data = dict()
run_data['feed_0'] = dict()
run_data['feed_0']['start_feed'] = str(datetime.datetime.now())
run_data['feed_0']['start_weight'] = .023
run_data['feed_0']['end_weight'] = .102
run_data['feed_0']['stable_weight'] = .107
run_data['feed_0']['details'] = [.023, .023, .023, .037, .054, .075, .102]

j_str = json.dumps(run_data)

print(j_str)

new_run_data = json.loads(j_str)

print(new_run_data['feed_0']['details'])