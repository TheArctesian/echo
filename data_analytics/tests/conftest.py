import pytest
from database.database import Database

@pytest.fixture
async def db():
    database = Database()
    await database.connect()
    return database
