"""Merge per-matchup JSON files into results/latest.json and a Markdown table."""
import glob, json, os, sys
from datetime import datetime, timezone

src, dst = sys.argv[1], sys.argv[2]
os.makedirs(dst, exist_ok=True)
parts = [json.load(open(p, encoding="utf-8")) for p in sorted(glob.glob(f"{src}/*.json"))]
decks = sorted({p["a"] for p in parts} | {p["b"] for p in parts})
stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

def rate(p, deck):
    played = p["games"]
    return None if not played else p["wins"][deck] / played

rows = ["| Deck | " + " | ".join(decks) + " | Gesamt |", "|---" * (len(decks) + 2) + "|"]
totals = {}
for d in decks:
    cells, w, g = [], 0, 0
    for o in decks:
        if o == d:
            cells.append("–"); continue
        p = next((x for x in parts if {x["a"], x["b"]} == {d, o}), None)
        if not p or not p["games"]:
            cells.append("?"); continue
        cells.append(f"{rate(p, d):.0%} ({p['wins'][d]}/{p['games']})")
        w += p["wins"][d]; g += p["games"]
    totals[d] = w / g if g else 0
    rows.append(f"| {d} | " + " | ".join(cells) + f" | **{totals[d]:.0%}** |")

md = [f"# Simulationsergebnisse", "", f"Stand: {stamp} · Forge KI gegen KI · Zeile = Siegquote dieses Decks gegen die Spalte", "", *rows, "",
      "## Rangliste", "", "| Platz | Deck | Siegquote |", "|---|---|---|"]
for i, (d, r) in enumerate(sorted(totals.items(), key=lambda x: -x[1]), 1):
    md.append(f"| {i} | {d} | {r:.0%} |")
errs = sum(p["errors"] for p in parts)
draws = sum(p["draws"] for p in parts)
md += ["", f"Unentschieden (Zeitlimit): {draws} · Fehler/abgebrochene Spiele: {errs}"]
open(f"{dst}/README.md", "w", encoding="utf-8").write("\n".join(md) + "\n")
json.dump({"updated": stamp, "matchups": parts, "overall": totals}, open(f"{dst}/latest.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\n".join(md))
