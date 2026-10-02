def plan(product, region):
    """Turn a product + region into a list of searches."""
    google = {"gl": "in"}
    steps = [
        {"engine": "google", "query": f"{product} cooperative {region}", "params": google},
        {"engine": "google", "query": f"{product} self help group {region}", "params": google},
        {"engine": "google", "query": f"{product} artisans {region} GI tag", "params": google},
        {"engine": "google", "query": f"{product} direct from producer {region}", "params": google},
        {"engine": "google_maps", "query": f"{product} {region}", "params": {"type": "search"}},
        {"engine": "google_news", "query": f"{product} {region} cooperative", "params": google},
    ]
    return steps