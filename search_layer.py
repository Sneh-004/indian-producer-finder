import os, json, hashlib
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("SERPAPI_KEY")
USE_MOCK = not KEY

if not USE_MOCK:
    import serpapi
    client = serpapi.Client(api_key=KEY)

# Fictional placeholder data shaped like real SerpApi responses.
# Use it only for building. The final demo must use real results.
MOCK = {
    "google": {"organic_results": [
        {"position": 1, "title": "SAMPLE Weavers Cooperative (demo)",
         "link": "https://example.com/weavers",
         "snippet": "Sample cooperative of handloom weavers in Odisha."},
        {"position": 2, "title": "SAMPLE Marketplace Listing (demo)",
         "link": "https://example.com/marketplace",
         "snippet": "Sample aggregator page selling sarees."},
    ]},
    "google_maps": {"local_results": [
        {"title": "SAMPLE Weavers Cooperative (demo)", "address": "Sample Road, Odisha",
         "phone": "0000000000", "rating": 4.3,
         "gps_coordinates": {"latitude": 20.0, "longitude": 85.0}},
    ]},
    "google_news": {"news_results": [
        {"title": "SAMPLE: Cooperative wins craft award (demo)",
         "link": "https://example.com/news", "source": {"name": "Sample News"},
         "date": "01/10/2026"},
    ]},
}

def search(query, engine="google", **params):
    if USE_MOCK:
        print(f"[MOCK MODE] {engine}: {query}")
        return MOCK.get(engine, {})
    os.makedirs("cache", exist_ok=True)
    key = hashlib.md5(f"{engine}|{query}|{params}".encode()).hexdigest()
    path = f"cache/{key}.json"
    if os.path.exists(path):
        print("Using saved result (no credit used)")
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    print("Calling SerpApi (1 credit used)")
    results = client.search(engine=engine, q=query, **params).as_dict()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    return results