import requests
import json

# Define the data to be sent in the request body
data = {
    "csi_data_x": [1, 2, 3, 4, 5],
    "csi_data_y": [6, 7, 8, 9, 10]
}

# Convert data to JSON format
json_data = json.dumps(data)

# Make the POST request
response = requests.post("http://localhost:8000/csi_data/both/raw/upload", json=data)

# Print the response
print(response.json())
