import pandas as pd
import json
from pandas import json_normalize

# Use curl to get the JSON data
json_data = !curl -s https://4fbc-2405-9800-b671-2af7-54ba-c2b0-542f-1287.ngrok-free.app/get_data

# Load JSON data
data_dict = json.loads(json_data[0])

data_dict['data'] = [{'Timestamp': item['Timestamp'], 'Data': item['Data']} for item in data_dict['data']]