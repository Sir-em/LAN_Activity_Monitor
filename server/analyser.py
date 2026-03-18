import time
from collections import defaultdict
from rules import evaluate_rules
from ml_model import predict_anomaly
from utils import calculate_risk_score

devices = {}
alerts = []
device_history = {}

TIME_WINDOW = 300  # 5 minutes


def update_device(log):
    ip = log["ip"]
    mac = log["mac"]
    timestamp = log["timestamp"]

    if ip not in devices:
        devices[ip] = {
            "ip": ip,
            "mac": mac,
            "first_seen": timestamp,
            "last_seen": timestamp,
            "join_count": 1,
            "leave_count": 0,
            "events": [timestamp],
            "history_mac": set([mac])
        }
    else:
        device = devices[ip]
        device["last_seen"] = timestamp
        device["join_count"] += 1
        device["events"].append(timestamp)
        device["history_mac"].add(mac)


def compute_features(device):
    now = time.time()

    recent_events = [t for t in device["events"] if now - t <= TIME_WINDOW]

    return {
        "session_duration": device["last_seen"] - device["first_seen"],
        "join_frequency": device["join_count"] / max(1, (device["last_seen"] - device["first_seen"])),
        "recent_activity": len(recent_events),
        "is_new": (now - device["first_seen"]) < 60,
        "ip_mac_mismatch": len(device["history_mac"]) > 1
    }



def analyze_device(ip, status):
    import time

    if ip not in device_history:
        device_history[ip] = {
            "first_seen": time.time(),
            "events": 1
        }
    else:
        device_history[ip]["events"] += 1

    score = 0
    rules = []

    # New device
    if device_history[ip]["events"] == 1:
        score += 2
        rules.append("NEW_DEVICE")

    # Frequent reconnects
    if device_history[ip]["events"] > 3:
        score += 3
        rules.append("HIGH_RECONNECT_RATE")

    return score, rules