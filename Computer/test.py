import requests
resp=requests.post("http://localhost:8000/map_data/upload",json={"map_data":[[0,0,0,0],[0,1,0,0],[0,0,0,0],[0,0,0,0]]})
print(resp.text)