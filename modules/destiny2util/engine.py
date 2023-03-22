from api import *
from update import *

with open(f'./data/destiny2util/en.json', 'r') as f:
    database = json.load(f)

langs = ('en', )
refresh(langs[0])


def search(w_type: str, perk1: str, perk2=None):
    res = []
    p1hash = None
    p2hash = None
    if perk1 in p2h:
        p1hash = p2h[perk1]
    else:
        raise Exception("Perk doesn't exist")
    if perk2 is not None:
        if perk2 in p2h:
            p2hash = p2h[perk1]
        else:
            raise Exception("Perk doesn't exist")

    p1lst = p2w[p1hash]
    p2lst = None
    if p2hash is not None:
        p2lst = p2w[p2hash]

    if p2lst is not None:
        for wpn in p1lst:
            if wpn in p2lst:
                res.append(wpn)
    else:
        res = p1lst

    print(len(p1lst))
    for wpn in res:
        pprint(database['DestinyInventoryItemDefinition'][wpn]['displayProperties']['name'])
