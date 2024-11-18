from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

'''Creating an async engine for the PostgreSQL database'''
engine = create_async_engine('postgresql+asyncpg://{username}:{password}@{host}/{database name}')

'''Creating an async session factory from the engine'''
local_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False,
                                   autocommit=False)
