import json
from enum import Enum

from redis_tools import redis_tools


class EventsMoneyLine(str, Enum):
    moneyline_home = '1'
    moneyline_away = '2'
    moneyline_draw = 'X'


class OddConverter:
    __ratio = 100

    @classmethod
    def pos_moneyline_to_odd(cls, moneyline: int):
        ratio = moneyline / cls.__ratio + 1
        return ratio

    @classmethod
    def neg_moneyline_to_odd(cls, moneyline: int):
        ratio = cls.__ratio / moneyline + 1
        return ratio

    def converter(self, moneyline: int):
        if moneyline < 0:
            res = self.neg_moneyline_to_odd(moneyline=abs(moneyline))
        else:
            res = self.pos_moneyline_to_odd(moneyline=moneyline)
        return res


odd_converter = OddConverter()


async def check_events_in_redis(sport_id: int):
    key = f'event: {sport_id}'
    cached_result = await redis_tools.get_pair(key=key)
    if cached_result:
        return json.loads(cached_result)
    else:
        return None


def func(events: list):
    pass
