from run_pipeline import run
from extraction import extract_cards
from ranking import rank_cards

out = run("handwoven saree", "Odisha")
cards, news = extract_cards(out)
ranked, removed = rank_cards(cards)

print()
print(f"{len(ranked)} ranked, {len(removed)} aggregators removed\n")
for i, c in enumerate(ranked, 1):
    print(f"{i}. {c['name']}  (score {c['score']})")
    for r in c["reasons"]:
        print("   -", r)
    print()