from scapy.all import ARP, Ether, srp, conf

def scan_network(ip_range="192.168.1.0/24"):
    conf.iface = "Wi-Fi"   # or "Ethernet" (check your adapter name)

    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")

    packet = ether / arp

    result = srp(packet, timeout=2, verbose=0)[0]

    devices = []

    for sent, received in result:
        devices.append({
            "ip": received.psrc,
            "mac": received.hwsrc
        })

    return devices