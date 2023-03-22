import json
import os
import random

database = {}

for i in os.listdir('./data/dcWoodFish'):
    name = i.split('.')
    name = name[0]
    with open(f"./data/dcWoodFish/{i}", "r") as f:
        database[name] = json.load(f)

# uid: str
# honor: int
# monks: int[8]
# broken: bool
# count: int

maxval = 100000
pcg = 5
base = maxval * pcg / 100
actual = []

for i in range(6):
    actual.append(base)
    base = base / 2


text = ["方丈", "两序", "堂主", "都监", "比丘", "沙弥"]


def process(uid: str):
    if uid not in database:
        database[uid] = {
            "uid": uid,
            "honor": 0,
            "monks": [0 for _ in range(6)],
            "broken": False,
            "count": 0
        }
    incr = knock(uid)

    database[uid]['count'] += 1
    if database[uid]['count'] % 50 == 0:
        tempf = open(f'./data/dcWoodFish/{uid}.json', 'w')
        json.dump(database[uid], tempf)

    return incr


def recruit(uid: str, count: int):
    res = [0 for _ in range(6)]
    for _ in range(count):
        r = random.choices([0, 1, 2, 3, 4, 5], [1, 8, 32, 64, 256, 512])
        res[r[0]] += 1
        database[uid]['monks'][r[0]] += 1
    if res[5] + res[4] >= 9:
        res[3] += 1
        res[2] += 1
        res[5] -= 2

    database[uid]['count'] += 1
    database[uid]['honor'] -= 1000
    if database[uid]['count'] % 5 == 0:
        tempf = open(f'./data/dcWoodFish/{uid}.json', 'w')
        json.dump(database[uid], tempf)

    return res


def knock_once():
    r = random.choices([1, 10, 100, 1000], [50, 39, 10, 1])
    r = r[0]
    return r


def knock(uid: str):
    lst = database[uid]['monks']
    res = knock_once()
    for x in range(len(lst)):
        val = lst[x] * actual[x]
        draw = random.randint(0, maxval)
        # print(val, draw)
        if draw < val:
            res += knock_once()
    if database[uid]['broken']:
        res *= -1
    else:
        b = random.randint(0, 1000)
        if b == 0:
            database[uid]['broken'] = True

    database[uid]['honor'] += res

    return res


def replace_wf(uid: str):
    if database[uid]['broken']:
        database[uid]['broken'] = False
        return True
    else:
        database[uid]['honor'] -= 100
        return False


def get_rank():
    lst = []
    for x in database:
        lst.append((x, database[x]['honor'] + 100 * sum(database[x]['monks'])))
    lst.sort(key=lambda x: x[1], reverse=True)
    if len(lst) > 5:
        lst = lst[0:5]
    return lst


def get_stats(uid: str):
    lst = database[uid]['monks']
    return lst
