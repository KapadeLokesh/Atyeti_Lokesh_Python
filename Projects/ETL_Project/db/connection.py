import sqlite3
from utils.constants import DB_NAME

def get_connection():
    return sqlite3.connect(DB_NAME)

