import json
import matplotlib.pyplot as plt
from datetime import datetime
timestamps = []
strength = []
with open("wifi_logs.jsonl","r") as f:
    for line in f:
        if "rssi" in line:
            df = json.loads(line)
            dates = datetime.strptime(df["time"], "%Y-%m-%d %H:%M:%S")
            timestamps.append(dates)
            strength.append(df["rssi"])
plt.plot(timestamps,strength, marker="o")
plt.ylabel("Signal Strength")
plt.xlabel("Time")
plt.title("RSSI Over Time")
plt.grid(True)
plt.show()
