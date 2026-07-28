import machine
import time
import network
from wificonfig import ssid, password
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
net.active(True)
net.connect(ssid,password)
max_cd = 15
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
    mac_string = mac_string[:len(mac_string)-1]
    print(f"MAC Address: {mac_string}")
    x = str(input("Press Enter to stop the program: ")).strip().lower()
    net.disconnect()
else:
    print(f"Error connecting to {ssid}")
    net.disconnect()

#while True:
#    signal = net.status("rssi") #strength signal
#    print(signal)
#    time.sleep(3)