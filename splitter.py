def calculate_split(parsed):
    total = parsed.get("total_amount", 0.0)
    participants = parsed.get("participants", [])
    splits = {}

    if not participants or total == 0.0:
        return {"error": "Invalid amount or no participants."}

    # Check for "uneven" keyword in original command
    if "uneven" in parsed.get("raw_text", "").lower():
        weights = [i + 1 for i in range(len(participants))]  # basic increasing weights
        total_weight = sum(weights)
        for p, w in zip(participants, weights):
            splits[p] = round(total * w / total_weight, 2)
    else:
        share = round(total / len(participants), 2)
        for p in participants:
            splits[p] = share

    return splits
