import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.database.db import Base, get_db_session
from main import app


TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_bookings.db"

test_engine = create_async_engine(TEST_DATABASE_URL)

test_session_factory = async_sessionmaker(
    bind=test_engine,
    expire_on_commit=False,
)


async def override_get_db_session():
    async with test_session_factory() as session:
        yield session


@pytest.fixture(autouse=True)
async def prepare_database():
    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client():
    app.dependency_overrides[get_db_session] = override_get_db_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as test_client:
        yield test_client

    app.dependency_overrides.clear()