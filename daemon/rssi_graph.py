import json
import matplotlib.pyplot as plt
from datetime import datetime
time = []
strength = []
with open("wifi_logs.jsonl","r") as f:
    for line in f:
        if "rssi" in line:
            df = json.loads(line)
            dates = datetime.strptime(df["time"], "%Y-%m-%d %H:%M:%S")
            time.append(dates)
            strength.append(df["rssi"])
print(time)
plt.plot(time,strength, marker="o")
plt.ylabel("Signal Strength")
plt.xlabel("Time")
plt.title("RSSI Over Time")
plt.grid(True)
plt.show()
