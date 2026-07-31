from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from settings import config

connect_args = {'check_same_thread': False}

engine = create_async_engine(config.DB_URL)

async def get_session():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
