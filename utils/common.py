import json
import random
import re
from typing import List

import geoip2.database
from fastapi import Request
from geoip2.errors import AddressNotFoundError

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


async def find_mentions(text: str) -> list[Floor]:
    """
    从文本中解析 mention
    """
    s = ' ' + text
    hole_ids = re.findall(r'[^#]#(\d+)', s)
    mentions: list[Floor] = []
    if hole_ids:
        hole_ids = list(map(lambda i: int(i), hole_ids))
        for id in hole_ids:
            floor = await Floor.filter(hole_id=id).first()
            if floor:
                mentions.append(floor)
    floor_ids = re.findall(r'##(\d+)', s)
    if floor_ids:
        floor_ids = list(map(lambda i: int(i), floor_ids))
        floors = await Floor.filter(id__in=floor_ids)
        mentions += floors
    return mentions


def get_ip(request: Request) -> str:
    x_forwarded_for: str = request.headers.get('x-forwarded-for')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[-1].strip()
    else:
        return request.client.host


ip_reader = geoip2.database.Reader('data/GeoLite2-City.mmdb')


def get_ip_location(ip: str) -> str:
    try:
        r = ip_reader.city(ip)
    except (AddressNotFoundError, ValueError):
        return ''
    country = r.country.names.get('zh-CN', '')
    city = r.city.names.get('zh-CN', '')
    return country + ' ' + city


def order_in_given_order(li: List[object], order: List[int]) -> List[object]:
    current = list(map(lambda x: x.id, li))
    result = []
    for i in order:
        try:
            key = current.index(i)
            result.append(li[key])
        except ValueError:
            pass
    return result
