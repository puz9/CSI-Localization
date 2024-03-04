import requests
from Serial_CSI_to_Web import get_map_data, csi_data_x,csi_data_y
api_url = "https://4fbc-2405-9800-b671-2af7-54ba-c2b0-542f-1287.ngrok-free.app/receive_data"
payload = {
    "map": get_map_data(csi_data_x,csi_data_y)

}

# Send a POST request to the FastAPI endpoint
response = requests.post(api_url, json=payload)