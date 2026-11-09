"""Print the GitHub Actions output line with all deck pairings (round robin)."""
import itertools, json, os, re, sys

arg = sys.argv[1] if len(sys.argv) > 1 else ""
focus = None
if arg.startswith("focus:"):  # only matchups of this one deck against all others
    focus, arg = arg[6:].strip(), ""
wanted = [d.strip() for d in arg.split(",") if d.strip()]
decks = sorted(f[:-4] for f in os.listdir("decks") if f.endswith(".dck"))
if wanted:
    decks = [d for d in decks if d in wanted]
slug = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
pairs = [{"a": a, "b": b, "id": f"{slug(a)}__vs__{slug(b)}"} for a, b in itertools.combinations(decks, 2) if not focus or focus in (a, b)]
print("pairs=" + json.dumps(pairs))
