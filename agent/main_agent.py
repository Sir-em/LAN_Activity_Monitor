import time
from arp_scanner import scan_network
from log_sender import send_log

SCAN_INTERVAL = 10  # seconds
known_devices = {}  # {ip: mac}


def create_log(ip, mac, status):
    return {
        "ip": ip,
        "mac": mac,
        "timestamp": time.time(),
        "status": status  # "online" or "offline"
    }


def main():
    print("LAN Monitoring Agent Started")

    global known_devices

    while True:
        try:
            current_devices = scan_network()

            # Convert list → dict for easy comparison
            current_dict = {d["ip"]: d["mac"] for d in current_devices}

            print("\nScanned Devices:", current_dict)

            # ✅ Detect NEW devices (JOIN)
            for ip, mac in current_dict.items():
                if ip not in known_devices:
                    print(f"[+] New Device: {ip} ({mac})")
                    log = create_log(ip, mac, "online")
                    send_log(log)

            # ✅ Detect REMOVED devices (LEAVE)
            for ip, mac in known_devices.items():
                if ip not in current_dict:
                    print(f"[-] Device Left: {ip} ({mac})")
                    log = create_log(ip, mac, "offline")
                    send_log(log)

            # 🔄 Update state
            known_devices = current_dict

            time.sleep(SCAN_INTERVAL)

        except Exception as e:
            print("Error in agent:", e)
            time.sleep(5)


if __name__ == "__main__":
    main()