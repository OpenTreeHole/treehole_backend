import json
import random
import re

from bbs.models import Floor

with open('utils/names.json', 'r', encoding='utf-8') as f:
    NAMES = json.load(f)

suffix = list('1234567890')


def random_name(compare_set: list) -> str:
    cnt = 0
    while cnt < 100:
        name = random.choice(NAMES)
        if name not in compare_set:
            return name
        else:
            cnt += 1
    while True:
        name = random.choice(NAMES) + random.choice(suffix)
        if name not in compare_set:
            return name
        else:
            pass


async def find_mentions(text: str) -> list[int]:
    """
    从文本中解析 mention
    Returns:  [<Floor>]
    """
    s = ' ' + text
    hole_ids = re.findall(r'[^#]#(\d+)', s)
    mentions = []
    if hole_ids:
        hole_ids = list(map(lambda i: int(i), hole_ids))
        for id in hole_ids:
            floor = await Floor.filter(hole_id=id).first().values_list('id', flat=True)
            mentions += floor
    floor_ids = re.findall(r'##(\d+)', s)
    if floor_ids:
        floor_ids = list(map(lambda i: int(i), floor_ids))
        floors = await Floor.filter(id__in=floor_ids).values_list('id', flat=True)
        mentions += floors
    return mentions
