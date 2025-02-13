from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


engine = create_async_engine(url="postgresql+asyncpg://root:MyPassword@postgres_db/mydb")

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass

async def get_db():
    async with async_session() as db:
        yield db

async def create_tables():
    async with engine.begin() as conn:
       await conn.run_sync(Base.metadata.create_all)

async def delete_tables():
   async with engine.begin() as conn:
       await conn.run_sync(Base.metadata.drop_all)