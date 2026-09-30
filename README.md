# Pico WiFi Manager

A MicroPython script for the Raspberry Pi Pico 2W that connects to WiFi, automatically retries on failure with exception handling, and contiguously reports connection status and signal strength (RSSI) to a Python daemon running on another machine over TCP socket. The daemon then logs the data in JSONL format, which can then be visualized with matplotlib.

## What it does

- Connects the Pico to WiFi with automatic retry logic (gives up after a configurable number of failed attempts)
- Once connected, checks connection health every 2 minutes and reports signal strength
- Sends structured WiFi data (timestamp, IP address, subnet, gateway, DNS, MAC, channel, RSSI) as JSON over TCP socket
- A receiver daemon on the host machine listens for these reports, accepts the connection, parses the JSON data and appends each one to a JSONL log file
- A separate script reads the log and plots signal strength over time using matplotlib
> *Note: The Pico side runs automatically on boot and so does the receiver as a systemd background service*

## Why I built this

Started with just testing the network module of the Raspberry pico I already had, and decided to go past WiFi connection basics and actually learn how to build a functional WiFi manager that can oversee it on it's own. Afterwards, I decided it would be a good time to learn about network sockets, as well as how to visualize the data I printed out on my console.

## Hardware

- Raspberry Pi Pico 2W (or any Micropython board that has WiFi support)

## Software Requirements

- Micropython on the Pico
- Python3 on the host machine, with `matplotlib` installed
> If you're on a Debian based Linux distrubition, it's simply:
```bash
sudo apt install python3-matplotlib
```
- Linux with systemd (for running the receiver as a background service)

## Installation

### 1. Pico side (MicroPython)

Copy `main.py` onto the Raspberry board via an IDE like Thonny, saved as `main.py` so it runs automatically on boot.

Rename `wificonfig-example.py` to `wificonfig.py` and fill in your own values:
- `ssid` / `password` — your WiFi credentials
- `host` — the local IP address of the machine running the receiver

### 2. Host side (Debian/Linux)

```bash
git clone https://github.com/agg-kantas/pico-wifi.git
cd pico-wifi
```

### 3. Run the receiver as a systemd service
```bash
sudo cp daemon/receiver.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable receiver.service
sudo systemctl start receiver.service
```
Check the status of the daemon:
```bash
sudo systemctl status receiver.service
```
> Logs are written to `daemon/wifi_logs.jsonl`
### 4. Visualize the data
```bash
cd daemon
python3 plot_rssi.py
```
