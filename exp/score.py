import json,sys,collections
d=json.load(open('results/latest.json'))
pref=sys.argv[1] if len(sys.argv)>1 else 'X '
r=collections.defaultdict(lambda:[0,0,{} ,0])
for m in d['matchups']:
  a=m['a']
  if not a.startswith(pref) or 'Friend' not in m['b']: continue
  if r[a][2].get(m['b']): continue   # newest first only
  w=m['wins'][a]; g=m['games']
  r[a][0]+=w; r[a][1]+=g; r[a][2][m['b']]=f"{w}/{g}"; r[a][3]+=m['errors']
for a,(w,g,det,e) in sorted(r.items(),key=lambda x:-x[1][0]/x[1][1]):
  print(f"{w/g*100:5.1f}%  {a:32s} BG {det.get('Friend Black-Green (Witherbloom)')}  BR {det.get('Friend Black-Red (Lorwyn Goblins)')} err {e}")
