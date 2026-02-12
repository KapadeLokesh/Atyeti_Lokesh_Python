import pytest
from db.connection import get_connection

@pytest.fixture
def db_conn():
    conn = get_connection()
    yield conn
    conn.close()
