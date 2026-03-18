def calculate_risk_score(rules, anomaly):
    weights = {
        "NEW_DEVICE": 2,
        "HIGH_RECONNECT_RATE": 4,
        "POSSIBLE_SPOOFING": 7,
        "NETWORK_SPIKE": 5
    }

    score = sum(weights.get(r, 0) for r in rules)

    if anomaly == "ANOMALY":
        score += 3

    return score