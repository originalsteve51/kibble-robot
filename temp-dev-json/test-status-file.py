import os.path
import json
from datetime import datetime 

class StatusFile():
    def __init__(self, file_path):
            if not file_path:
                self.file_path = None
                self.status_json = None
                raise Exception('You must provide a path-name for the status file.')
            self.file_path = file_path
            if os.path.isfile(file_path):
                # Existing file, load it so it can be added to or retrieved
                j_file = open(file_path, 'r')
                self.status_json = json.load(j_file)
                j_file.close()
            else:
                # New file... Start it with no entries
                self.status_json = dict()
                self.status_json['entries'] = dict() # list()
                j_file = open(file_path, 'w')
                json.dump(self.status_json, j_file, indent=4)
                j_file.close()
    
    def add_status(self, o_json):
        if self.status_json:
            # Open file for read/write
            j_file = open(self.file_path, 'r+')
            self.status_json = json.load(j_file)
            date_time = get_date_time()
            self.status_json['entries'][f'{date_time[0]}--{date_time[1]}'] = o_json
            # We read the file above, set the file position back to the start 
            # before writing everything (including the addition) back out to it
            j_file.seek(0)
            json.dump(self.status_json, j_file) # , indent=4)
            j_file.close()

    def status_as_json(self):
        if self.file_path and os.path.isfile(self.file_path):
            file = open(self.file_path, 'r')
            o_json = json.load(file)
            file.close()
            return o_json

def get_date_time():
    current_date = datetime.strftime(datetime.now(),"%m/%d/%Y")
    current_time = datetime.strftime(datetime.now(),"%H:%M:%S")
    return current_date, current_time 

if __name__ == '__main__':
    status_file = StatusFile('./status.json')

    date_time = get_date_time()
    current_date = date_time[0]
    current_time = date_time[1]

    entry = dict()

    entry['start_feed'] = current_time
    entry['start_weight'] = .023
    entry['end_weight'] = .102
    entry['stable_weight'] = .107
    entry['details'] = [.023, .023, .023, .037, .054, .075, .102]

    status_file.add_status(entry)

    json_status = status_file.status_json
    print(f'There are {len(json_status["entries"])} entries in the file.')
    for key in json_status['entries']:
        print(key)

    #print(status_file.status_as_json())

