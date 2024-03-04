import serial
import csv
ser = serial.Serial('COM8', 921600)

f=open('csi_data.csv', mode='w')

while True:
    try:
        line = ser.readline().decode().strip()  # Read a line and decode it from bytes to string
        if line.startswith("type,"):
            csi_data_writer=csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csi_data_writer.writerow(line.split(","))
        if line.startswith("CSI_DATA"):

            print(line)
            # Extract the array of values from the line
            data_str = line.split(",")[-1]  # Get the last part of the line which contains the array
            data_str = data_str[1:-1]  # Remove brackets from the array
            data_values = [int(x) for x in data_str.split()]  # Convert the space-separated string into a list of integers
            print("Received data:", data_values)  # Do whatever analysis or processing you need with the data
            
            

    except UnicodeDecodeError as e:
        print("Error decoding line:", e)
        continue
    except KeyboardInterrupt:
        print("Exiting...")
        break
    except ValueError as e:
        print("ValueError")
        continue
f.close()