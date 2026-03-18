from flask import Flask, request, jsonify

app = Flask(__name__)

logs = []
devices = {}  # ip → latest state


# ✅ Analyzer
device_history = {}

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

    if device_history[ip]["events"] == 1:
        score += 2
        rules.append("NEW_DEVICE")

    if device_history[ip]["events"] > 3:
        score += 3
        rules.append("HIGH_RECONNECT_RATE")

    return score, rules


# ✅ Update device state
def update_device(log):
    ip = log["ip"]

    devices[ip] = {
        "mac": log["mac"],
        "status": log["status"],
        "last_seen": log["timestamp"]
    }


# ✅ Receive logs
@app.route("/log", methods=["POST"])
def receive_log():
    log = request.json

    update_device(log)

    score, rules = analyze_device(log["ip"], log["status"])

    enriched_log = {
        "ip": log["ip"],
        "mac": log["mac"],
        "status": log["status"],
        "timestamp": log["timestamp"],
        "risk_score": score,
        "rules": rules,
        "anomaly": "HIGH" if score > 5 else "NORMAL"
    }

    logs.append(enriched_log)

    return jsonify({"status": "received"})


# ✅ Get logs
@app.route("/logs")
def get_logs():
    return jsonify(logs)


# ✅ Summary for dashboard
@app.route("/summary")
def summary():
    total = len(devices)
    online = sum(1 for d in devices.values() if d["status"] == "online")
    offline = total - online

    return jsonify({
        "total": total,
        "online": online,
        "offline": offline
    })


# ✅ Device table
@app.route("/devices")
def get_devices():
    return jsonify(devices)


if __name__ == "__main__":
    app.run(debug=True)