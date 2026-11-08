"""Turn a Forge sim log into a JSON result: wins per deck, draws, game times."""
import json, re, sys

a, b, log = sys.argv[1], sys.argv[2], sys.argv[3]
text = open(log, encoding="utf-8", errors="ignore").read()
names = {}
for i, deck in ((1, a), (2, b)):
    m = re.search(rf"Ai\({i}\)-(.+?)(?: vs | - \d+ game)", text)
    names[deck] = f"Ai({i})-" + (m.group(1).strip() if m else deck)

res = {"a": a, "b": b, "wins": {a: 0, b: 0}, "draws": 0, "games": 0, "ms": [], "errors": 0}
for m in re.finditer(r"Game Result: Game \d+ ended in (\d+) ms\. (.+?) has won!", text):
    res["games"] += 1
    res["ms"].append(int(m.group(1)))
    for deck, n in names.items():
        if m.group(2).strip() == n:
            res["wins"][deck] += 1
res["draws"] = len(re.findall(r"ended in a Draw", text))
res["games"] += res["draws"]
res["errors"] = len(re.findall(r"threw exception|Could not load deck", text))
print(json.dumps(res, ensure_ascii=False))
