import json
from pprint import pprint

h2p = dict()
p2h = dict()
p2w = dict()


def refresh(lang: str):
    print(f"Refreshing {lang}")
    with open(f'./data/destiny2util/{lang}.json', 'r') as f:
        database = json.load(f)

    database: dict
    processed = {}
    for k, v in database['DestinyInventoryItemDefinition'].items():
        if v['itemType'] == 3:
            try:
                item_hash = str(v['hash'])
                name = v['displayProperties']['name']
                element = v['defaultDamageType']
                bucket = v['inventory']['bucketTypeHash']
                sockets = []

                if item_hash == "3653573172":
                    print(k, v['displayProperties']['name'])

                if 'sockets' not in v:
                    continue

                for iv in v['sockets']['socketEntries']:
                    if iv['plugSources'] == 2 and "randomizedPlugSetHash" in iv:
                        sockets.append(str(iv['randomizedPlugSetHash']))
                if len(sockets) != 4:
                    continue
                if item_hash in processed:
                    raise Exception("ERROR")
                processed[item_hash] = {
                    "name": name,
                    "bucket": bucket,
                    "element": element,
                    "sockets": sockets,
                }
            except KeyError as e:
                print(e)
                pprint(v)
                with open("./temp.json", 'w') as f:
                    json.dump(v, f)
                break

    def process_weapon(wpn_hash: str, payload: dict):
        def _process(perkset_hash: str):
            perkset = database['DestinyPlugSetDefinition'][perkset_hash]
            for plug in perkset['reusablePlugItems']:
                perk_hash = str(plug['plugItemHash'])
                perk = database['DestinyInventoryItemDefinition'][perk_hash]
                if perk['itemTypeDisplayName'] == "Enhanced Trait":
                    continue
                if perk_hash not in h2p:
                    h2p[perk_hash] = {
                        lang: perk['displayProperties']['name']
                    }
                    p2h[perk['displayProperties']['name']] = perk_hash
                    p2w[perk_hash] = [wpn_hash]
                else:
                    if lang not in h2p[perk_hash]:
                        h2p[perk_hash][lang] = perk['displayProperties']['name']
                    elif wpn_hash not in p2w[perk_hash]:
                        p2w[perk_hash].append(wpn_hash)

        _process(payload["sockets"][-1])
        _process(payload["sockets"][-2])

    for k, v in processed.items():
        process_weapon(k, v)

    del database

    return h2p, p2h, p2w
