from search_layer import search

results = search("handwoven saree cooperative Odisha", gl="in")
for r in results.get("organic_results", []):
    print(r["title"])
    print(r["link"])
    print()