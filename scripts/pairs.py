"""Print the GitHub Actions output line with all deck pairings (round robin)."""
import itertools, json, os, re, sys

wanted = [d.strip() for d in (sys.argv[1] if len(sys.argv) > 1 else "").split(",") if d.strip()]
decks = sorted(f[:-4] for f in os.listdir("decks") if f.endswith(".dck"))
if wanted:
    decks = [d for d in decks if d in wanted]
slug = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
pairs = [{"a": a, "b": b, "id": f"{slug(a)}__vs__{slug(b)}"} for a, b in itertools.combinations(decks, 2)]
print("pairs=" + json.dumps(pairs))
