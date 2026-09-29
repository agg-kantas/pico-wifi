import json
import pandas as pd
import matplotlib as plt
Y = []
X = []
with open("wifi_logs.jsonl","r") as f:
    for line in f:
        if "rssi" in line:
            df = json.loads(line)
            Y.append(df["time"])
            X.append(df["rssi"])
# df1 = pd.DataFrame(Y)
