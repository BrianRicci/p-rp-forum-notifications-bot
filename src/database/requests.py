from database.models import async_session
from database.models import User, Topic

from sqlalchemy import select


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def get_user_topics(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        topics = user.topics
        
        if topics:
            return topics
        
        return 'Список топиков пуст'


async def set_topic(tg_id, topic_url):
    # здесь нужно получить из парсера все данные о топике
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        # session.add(Topic(name=name,
        #                     url=url,
        #                     messages_number=messages_number,
        #                     user_id=user.id))
        # await session.commit()


async def get_topic_list():
    async with async_session() as session:
        results = await session.execute(select(Topic)) 
        topics = results.scalars().all()

        return topics
