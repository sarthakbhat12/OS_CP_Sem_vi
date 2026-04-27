# system/comparator.py

def compare(results):
    """
    Prints comparison table and highlights best algorithm
    """

    print("\n====== CPU COMPARISON TABLE ======")

    for r in results:
        print(f"{r['name']:25} | Avg WT = {r['avg_wt']:.2f}")

    # find best algorithm
    best = min(results, key=lambda x: x["avg_wt"])

    print("\n👉 Best Algorithm:", best["name"], 
          f"(WT = {best['avg_wt']:.2f})")