from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from .settings import config

engine = create_async_engine(config.db_url)
AsyncSession = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with AsyncSession() as session:
        yield session
