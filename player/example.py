import asyncio
import os
import sys

from fastapi import Depends
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
sys.path.insert(0, os.path.split(dir_path)[0])
from db_helper import session_factory, async_session
from player.models import Player

db = async_session()


@event.listens_for(Player, 'after_update')
def bet_after_update(connection, target, mapper=None):
    if target.matches == 103:
        print('Good')


# asyncio.run(listen_for_bet_updates(session=db))
bet_after_update(connection=db, target=Player)
