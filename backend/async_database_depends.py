from backend.async_database import local_session
from sqlalchemy.ext.asyncio import AsyncSession


async def get_database() -> AsyncSession:
    '''get_database generates an async session for the database'''
    async with local_session() as session:
        yield session
