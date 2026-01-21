from db.connection import get_connection

def execute_query(query, params=None, fetch=False):
    conn = get_connection()
    if not conn:
        raise Exception("Database connection failed")

    cursor = conn.cursor(dictionary=True)

    cursor.execute(query, params or ())

    result = None
    if fetch:
        result = cursor.fetchall()

    conn.commit()
    cursor.close()
    conn.close()

    return result
