def evaluate_rules(features, total_devices):
    rules = []

    if features["join_frequency"] > 0.05:
        rules.append("HIGH_RECONNECT_RATE")

    if features["is_new"]:
        rules.append("NEW_DEVICE")

    if features["ip_mac_mismatch"]:
        rules.append("POSSIBLE_SPOOFING")

    if total_devices > 20:
        rules.append("NETWORK_SPIKE")

    return rules