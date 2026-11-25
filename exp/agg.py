import json,collections,sys
d=json.load(open('results/latest.json'))
opp=('Friend Black-Green (Witherbloom)','Friend Black-Red (Lorwyn Goblins)','White-Blue Humans')
r=collections.defaultdict(lambda:collections.defaultdict(lambda:[0,0]))
for m in d['matchups']:
  a=m['a']
  if a.startswith(sys.argv[1]) and m['b'] in opp and m['games']>=150:
    x=r[a][m['b']]; x[0]+=m['wins'][a]; x[1]+=m['games']
for a,v in sorted(r.items(),key=lambda x:-sum(w for w,g in x[1].values())/sum(g for w,g in x[1].values())):
  w=sum(x[0] for x in v.values()); g=sum(x[1] for x in v.values())
  print(f"{w/g*100:5.1f}% n={g:4d} {a:26s}", ' '.join(f"{o.split()[1][:5]}{'/'+o.split()[-1][:4] if 'Friend' in o else ''}:{v[o][0]}/{v[o][1]}" for o in opp if o in v))
