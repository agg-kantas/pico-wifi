import socket
import json
import time
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) # Socket Option Reuse Address
s.bind(("",8080)) # "" IP address just means the receiver accepts any network interface the machine host has, better than using the actual IP that can change for multiple reasons
s.listen(5)
while True:
    connection, client_address = s.accept()
    data = connection.recv(1024)
    data = json.loads(data)
    with open ("wifi_logs.jsonl","a") as f:
        f.write(json.dumps(data) + "\n")
s.close()


