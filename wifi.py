import machine
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
def options():
    ip,subnet,gateway,dns = net.ifconfig()
    print(f"IP: {ip}\n"
        f"Subnet Mask: {subnet}\n"
        f"Default Gateway: {gateway}\n"
        f"DNS Configuration: {dns}\n")
    channel_id = net.config("channel")
    print(f"Channel ID: {channel_id}")
    mac_bytes = net.config("mac")
    mac = bytes.hex(mac_bytes)
    mac_string = ""
    for i in range(0,len(mac),2):
        mac_string = mac_string + mac[i:i+2]+":"
    mac_string = mac_string[:-1]
    print(f"MAC Address: {mac_string}")


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
        options()
        port = 8080
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creates an IPv4 TCP protocol socket
        try:
            s.connect((host,port))
            s.send("Data sent successfully")
        except OSError as e:
            print(f"Socket Error: {e}")

        time.sleep(100)
        while True:
            connected = net.isconnected() #check connection again
            if connected == True:
                signal = net.status("rssi") #Received Signal Strength Indicator
                print(f"Connection secure at {signal} dBm signal strength") #
                time.sleep(100)
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
        time.sleep(1)
        print(f"Attempt #{count} at reconnection to {ssid}")
        net.disconnect() #disconnect cleanly before reconnecting
        continue


