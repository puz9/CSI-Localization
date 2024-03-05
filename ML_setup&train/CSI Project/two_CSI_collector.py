import serial
import threading
import csv
import keyboard as kb
# Define serial ports for each ESP device
port_x = "COM8" #channel 4
port_y = "COM15" #channel 11

baudrate=921600



fx_csv,writer_x=None,None
fy_csv,writer_y=None,None

def reload_csv():
    global fx_csv,writer_x,fy_csv,writer_y
    column_str="type,role,mac,rssi,rate,sig_mode,mcs,bandwidth,smoothing,not_sounding,aggregation,stbc,fec_coding,sgi,noise_floor,ampdu_cnt,channel,secondary_channel,local_timestamp,ant,sig_len,rx_state,real_time_set,real_timestamp,len,CSI_DATA"
    if fx_csv:
        fx_csv.close()
    if fy_csv:
        fy_csv.close()
    fx_csv=open('csi_data_x.csv', 'w', newline='\n')
    writer_x = csv.writer(fx_csv)
    writer_x.writerow(column_str.split(","))
    fy_csv=open('csi_data_y.csv', 'w', newline='\n')
    writer_y = csv.writer(fy_csv)
    writer_y.writerow(column_str.split(","))

reload_csv()
def read_serial(port, axis):
    global writer_x,writer_y
    global baudrate
    ser = serial.Serial(port, baudrate=baudrate, timeout=1)
    ser.flushInput()
    ser.flushOutput()
    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            print(line)
            if line.startswith("type,"):
                reload_csv()
            if line.startswith("CSI_DATA"):
                if axis=="X":
                    writer=writer_x
                elif axis=="Y":
                    writer=writer_y
                writer.writerow(line.split(","))
            if kb.is_pressed('q'):
                break
        except KeyboardInterrupt:
            break
        except UnicodeDecodeError as e:
            print(e)
            continue
        except serial.SerialException as e:
            print(e)
            continue
    ser.close()
    if axis=="X":
        fx_csv.close()
    elif axis=="Y":
        fy_csv.close()

if __name__ == "__main__":
    # Create and start threads for reading from each serial port
    thread_x = threading.Thread(target=read_serial, args=(port_x, "X"))
    # thread_y = threading.Thread(target=read_serial, args=(port_y, "Y"))

    thread_x.start()
    # thread_y.start()

    # Keep the main thread running
    # while True:
        # pass
