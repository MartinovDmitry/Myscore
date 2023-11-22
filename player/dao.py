# from sqlalchemy import insert, select, and_
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from player.models import Player
# from player.schemas import SchPlayerCreate


# class PlayerDAO:
#     model = Player
#
#     @classmethod
#     async def create_player(cls, player: SchPlayerCreate, session: AsyncSession):
#         stmt = insert(cls.model).values(**player.model_dump())
#         await session.execute(stmt)
#         await session.commit()
#
#     @classmethod
#     async def get_player_by_name(cls, session: AsyncSession, first_name: str, second_name: str):
#         query = select(cls.model).where(and_(cls.model.first_name == first_name, cls.model.second_name == second_name))
#         result = await session.execute(query)
#         players = result.scalars().all()
#         return players
