from urllib.parse import urlparse

AGGREGATORS = ["indiamart", "amazon", "flipkart", "alibaba", "meesho",
               "justdial", "tradeindia", "etsy", "ebay"]

TYPES = {
    "Cooperative": ["cooperative", "co-operative", "society"],
    "SHG": ["self help group", "self-help group", "shg"],
    "Artisan": ["artisan", "weaver", "craft"],
}


def detect_type(text):
    t = text.lower()
    for label, words in TYPES.items():
        if any(w in t for w in words):
            return label
    return "Unknown"


def is_aggregator(url):
    host = urlparse(url).netloc.lower()
    return any(a in host for a in AGGREGATORS)


def has_gi(text):
    t = text.lower()
    return "gi tag" in t or "geographical indication" in t


def extract_cards(results):
    cards = {}
    news = []
    for item in results:
        engine = item["step"]["engine"]
        data = item["data"]

        if engine == "google":
            for r in data.get("organic_results", []):
                link = r.get("link", "")
                if not link or link in cards:
                    continue
                text = f'{r.get("title", "")} {r.get("snippet", "")}'
                cards[link] = {
                    "name": r.get("title", ""),
                    "link": link,
                    "type": detect_type(text),
                    "aggregator": is_aggregator(link),
                    "gi": has_gi(text),
                    "snippet": r.get("snippet", ""),
                    "address": None, "phone": None, "rating": None,
                }

        elif engine == "google_maps":
            for r in data.get("local_results", []):
                key = "maps:" + r.get("title", "")
                if key in cards:
                    continue
                cards[key] = {
                    "name": r.get("title", ""),
                    "link": r.get("website", ""),
                    "type": detect_type(r.get("title", "")),
                    "aggregator": False,
                    "gi": False,
                    "snippet": "",
                    "address": r.get("address"),
                    "phone": r.get("phone"),
                    "rating": r.get("rating"),
                }

        elif engine == "google_news":
            for r in data.get("news_results", []):
                news.append({"title": r.get("title", ""), "link": r.get("link", "")})

    return list(cards.values()), news