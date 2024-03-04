import requests
import serial


ser = serial.Serial('COM8', 921600)
while True:
    try:
        line = ser.readline().decode().strip()  # Read a line and decode it from bytes to string
        if line.startswith("CSI_DATA"):
            # Extract the array of values from the line
            data_str = line.split(",")[-1]  # Get the last part of the line which contains the array
            data_str = data_str[1:-1]  # Remove brackets from the array
            data_values = [int(x) for x in data_str.split()]  # Convert the space-separated string into a list of integers
            # print("Received data:", data_values)  # Do whatever analysis or processing you need with the data
            url = "http://192.168.28.18:8000/upload_csi_dataX"
            payload = {"csi_data": data_values}
            response = requests.post(url, json=payload)
            # print(response.json())
            print("already sent to server")
    except UnicodeDecodeError as e:
        print("Error decoding line:", e)
        continue
    except KeyboardInterrupt:
        print("Exiting...")
        break
    except ValueError as e:
        print("Error decoding line:", e)
        continue
# Close serial port
ser.close()