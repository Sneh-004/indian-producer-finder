def score_card(card):
    score = 0
    reasons = []

    if card["type"] in ("Cooperative", "SHG"):
        score += 3
        reasons.append(f"Identified as a {card['type']}")
    elif card["type"] == "Artisan":
        score += 2
        reasons.append("Identified as an artisan/producer")

    if card["gi"]:
        score += 3
        reasons.append("Mentions GI tag / geographical indication")

    if card["phone"]:
        score += 1
        reasons.append("Has a phone number")
    if card["address"]:
        score += 1
        reasons.append("Has a physical address")
    if card["rating"] and card["rating"] >= 4:
        score += 1
        reasons.append(f"Rated {card['rating']} on Maps")

    if not reasons:
        reasons.append("No strong signals found")
    return score, reasons


def rank_cards(cards):
    ranked, removed = [], []
    for c in cards:
        if c["aggregator"]:
            removed.append(c)
            continue
        score, reasons = score_card(c)
        ranked.append({**c, "score": score, "reasons": reasons})
    ranked.sort(key=lambda c: c["score"], reverse=True)
    return ranked, removed