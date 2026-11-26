import json,collections,sys
d=json.load(open('results/latest.json'))
opp=['Friend Black-Green (Witherbloom)','Opp BG-B Aggro Pests','Friend Black-Red (Lorwyn Goblins)','Opp BR-B Goblin Burn']
G=int(sys.argv[1]); pref=sys.argv[2:]
r=collections.defaultdict(dict)
for m in d['matchups']:
  if m['games']==G and m['b'] in opp and m['b'] not in r[m['a']] and any(m['a'].startswith(p) for p in pref): r[m['a']][m['b']]=m['wins'][m['a']]
for a,v in sorted(r.items(),key=lambda x:-sum(x[1].values())/max(1,len(x[1]))):
  print(f"{sum(v.values())/len(v)/G*100:5.1f}% {a:28s}",' '.join(f"{v.get(o,'--'):>3}" for o in opp),'' if len(v)==4 else 'INCOMPLETE')
