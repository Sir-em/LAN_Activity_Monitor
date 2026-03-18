import requests
import pandas as pd
import streamlit as st
from datetime import datetime

SERVER_URL = "http://127.0.0.1:5000/logs"

st.set_page_config(page_title="LAN Log Analyzer", layout="wide")

st.title("Centralized LAN Monitoring Dashboard")


def fetch_logs():
    try:
        response = requests.get(SERVER_URL, timeout=2)
        return response.json()
    except:
        return []


logs = fetch_logs()

if len(logs) == 0:
    st.warning("No logs received yet")
    st.stop()

df = pd.DataFrame(logs)

# ---- Timestamp Conversion ----
if "timestamp" in df.columns:
    df["timestamp"] = df["timestamp"].apply(
        lambda x: datetime.fromtimestamp(x)
    )

# ---- Show Events ----
st.subheader("Recent Events")
st.dataframe(
    df.sort_values("timestamp", ascending=False),
    use_container_width=True
)

# ---- Device Status Logic ----
device_status = {}

for _, row in df.iterrows():

    ip = row.get("device_ip") or row.get("ip")
    event = row.get("event")

    if event == "DEVICE_JOINED":
        device_status[ip] = "ONLINE"

    elif event == "DEVICE_LEFT":
        device_status[ip] = "OFFLINE"

# ---- Metrics ----
total_devices = len(device_status)
online_devices = list(device_status.values()).count("ONLINE")
offline_devices = list(device_status.values()).count("OFFLINE")

col1, col2, col3 = st.columns(3)

col1.metric("Total Devices", total_devices)
col2.metric("Online Devices", online_devices)
col3.metric("Offline Devices", offline_devices)

# ---- Device Table ----
status_table = []

for ip, status in device_status.items():
    status_table.append({
        "Device IP": ip,
        "Status": status
    })

status_df = pd.DataFrame(status_table)

st.subheader("Device Status")
st.dataframe(status_df, use_container_width=True)

# ---- NEW: Risk Section (if available) ----
if "risk_score" in df.columns:
    st.subheader("High Risk Devices")
    st.dataframe(df[df["risk_score"] >= 4])