import os

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_async_engine(url=DATABASE_URL)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass

async def get_db():
    async with async_session() as db:
        yield db

