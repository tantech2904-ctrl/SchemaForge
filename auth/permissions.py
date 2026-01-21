from db.connection import get_connection

def has_permission(role, table, action):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM permissions
        WHERE role=%s AND table_name=%s
    """, (role, table))

    perm = cursor.fetchone()
    conn.close()

    if not perm:
        return False

    return perm.get(f"can_{action}", False)

