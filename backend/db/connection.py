import mysql.connector
from mysql.connector import pooling
from core.config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

_pool = pooling.MySQLConnectionPool(
    pool_name="schemaforge_pool",
    pool_size=5,
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
)

def get_connection():
    return _pool.get_connection()
