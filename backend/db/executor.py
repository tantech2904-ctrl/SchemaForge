from db.connection import get_connection

def execute_query(
    query: str,
    params: tuple = (),
    fetch: bool = False,
    fetchone: bool = False
):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(query, params)

        if fetchone:
            result = cursor.fetchone()
        elif fetch:
            result = cursor.fetchall()
        else:
            result = None

        conn.commit()
        return result

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()
