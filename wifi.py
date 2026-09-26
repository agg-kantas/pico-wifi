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
    data = {
        "ip":ip,
        "subnet":subnet,
        "gateway":gateway,
        "dns":dns,
        "channel_id":channel_id,
        "mac":mac_string
        }
    return data

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
        print(f"IP: {data["ip"]}\n"
        f"Subnet Mask: {data["subnet"]}\n"
        f"Default Gateway: {data["gateway"]}\n"
        f"DNS Configuration: {data["dns"]}\n"
        f"Channel ID: {data["channel_id"]}\n"
        f"MAC Address: {data["mac"]}\n")
        port = 8080
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creates an IPv4 TCP protocol socket
        try:
            s.connect((host,port))
            s.send("Connection made successfully!\n")
            json_string = json.dumps(data)
            s.send(json_string)
            s.close()
        except OSError as e:
            print(f"Socket Error: {e}")
            s.close()
        time.sleep(120)
        while True:
            connected = net.isconnected() #check connection again
            if connected == True:
                signal = net.status("rssi") #Received Signal Strength Indicator
                print(f"Connection secure at {signal} dBm signal strength") #
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


