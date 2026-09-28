import machine
import json
import time
import network
from wificonfig import ssid, password, host
import socket
status_text = {
    -3 : "CYW43_LINK_BADAUTH",
    -2 : "CYW43_LINK_NONET",
    -1 : "CYW43_LINK_FAIL",
    0 : "CYW43_LINK_DOWN",
    1 : "CYW43_LINK_JOIN",
    2 : "CYW43_LINK_NOIP",
    3 : "CYW43_LINK_UP"
    }
net = network.WLAN(network.STA_IF) # interface to connect to a station

def get_data():
    ip,subnet,gateway,dns = net.ifconfig()
    channel_id = net.config("channel")
    mac_bytes = net.config("mac")
    mac = bytes.hex(mac_bytes)
    mac_string = ""
    for i in range(0,len(mac),2):
        mac_string = mac_string + mac[i:i+2]+":"
    mac_string = mac_string[:-1]
    time_string = get_time()
    data = {
        "time":time_string,
        "ip":ip,
        "subnet":subnet,
        "gateway":gateway,
        "dns":dns,
        "channel_id":channel_id,
        "mac":mac_string
        }
    return data

def connect_socket(data):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creates an IPv4 TCP protocol socket
    try:
        s.connect((host,port))
        print("Socket connection made successfully!")
        json_string = json.dumps(data)
        s.send(json_string)
        time.sleep(1)
        s.close()
    except OSError as e:
        print(f"Socket Error: {e}")
        s.close()

def get_time():
    t = time.gmtime()
    time_string = (f"{t[0]}-{t[1]:02d}-{t[2]:02d} {t[3]:02d}:{t[4]:02d}:{t[5]:02d}") #converts time in seconds to a string timestamp with zeros padding
    return time_string

port=8080
count=0
while True:
    net.active(True)
    net.connect(ssid,password)
    max_cd = 8
    while max_cd >0:
        status = net.status()
        print(status_text[status])
        connected = net.isconnected()
        if connected==True:
            break
        else:
            time.sleep(1)
            max_cd = max_cd - 1
    if connected == True:
        print(f"Connected to {ssid} successfully!")
        count=0
        data = get_data()
        print(f"Time: {data["time"]}\n"
        f"IP: {data["ip"]}\n"
        f"Subnet Mask: {data["subnet"]}\n"
        f"Default Gateway: {data["gateway"]}\n"
        f"DNS Configuration: {data["dns"]}\n"
        f"Channel ID: {data["channel_id"]}\n"
        f"MAC Address: {data["mac"]}\n")
        time.sleep(1)
        connect_socket(data)
        time.sleep(120)
        while True:
            connected = net.isconnected() #check connection again
            if connected == True:
                signal = net.status("rssi") #Received Signal Strength Indicator
                time_string = get_time()
                print(f"Time: {time_string}")
                print(f"Connection secure at {signal} dBm signal strength")
                rssi_data = {
                            "time":time_string,
                            "rssi":signal
                             }
                connect_socket(rssi_data)
                time.sleep(120)
            else:
                print(f"Lost connection to {ssid}, attempting reconnect...")
                net.disconnect() #disconnect cleanly before reconnecting
                break
    elif connected == False and count >=10:
        print(f"Error connecting to {ssid}")
        print(f"Multiple failed attempts of reconnection to {ssid}, disconnecting permanently.")
        net.disconnect()
        break
    else:
        print(f"Error connecting to {ssid}, will retry in 60 seconds")
        count=count+1
        time.sleep(60)
        print(f"Attempt #{count} at reconnection to {ssid}")
        net.disconnect() #disconnect cleanly before reconnecting
        continue

