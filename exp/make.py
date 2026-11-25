"""Make variant decks: python3 exp/make.py spec.json  -> writes decks/X <name>.dck, prints names"""
import json, re, sys
def load(name):
    d = {}
    for l in open(f'decks/{name}.dck', encoding='utf-8'):
        m = re.match(r'(\d+) (.+)\|(\w+)$', l.strip())
        if m: d[(m.group(2), m.group(3))] = d.get((m.group(2), m.group(3)), 0) + int(m.group(1))
    return d
def apply(d, cuts, adds):
    d = dict(d)
    for nm, n in cuts.items():
        k = next(k for k in d if k[0] == nm); d[k] -= n
        assert d[k] >= 0, nm
        if not d[k]: del d[k]
    for nm, n in adds.items():
        nm, ed = (nm.split('|') + ['LTR'])[:2]
        d[(nm, ed)] = d.get((nm, ed), 0) + n
    assert sum(d.values()) == 60, (sum(d.values()), cuts, adds)
    return d
def write(name, d):
    open(f'decks/{name}.dck', 'w', encoding='utf-8').write(f'[metadata]\nName={name}\n[Main]\n' + ''.join(f'{n} {k}|{e}\n' for (k, e), n in d.items()))
spec = json.load(open(sys.argv[1], encoding='utf-8'))
names = []
for base, variants in spec.items():
    b = load(base)
    for v in variants:
        name = 'X ' + v['name']
        write(name, apply(b, v.get('cut', {}), v.get('add', {}))); names.append(name)
print(','.join(names))
