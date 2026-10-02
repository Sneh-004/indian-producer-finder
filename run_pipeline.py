from planner import plan
from search_layer import search


def run(product, region):
    results = []
    for step in plan(product, region):
        data = search(step["query"], engine=step["engine"], **step["params"])
        results.append({"step": step, "data": data})
    return results


if __name__ == "__main__":
    out = run("handwoven saree", "Odisha")
    for item in out:
        print(item["step"]["engine"], "|", item["step"]["query"])