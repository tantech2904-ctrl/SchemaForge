from db.executor import execute_query
from db.metadata import is_valid_table


def get_all_rows(table):
    if not is_valid_table(table):
        raise Exception("Invalid table")

    sql = f"SELECT * FROM {table}"
    return execute_query(sql, fetch=True)


def get_row_by_id(table, row_id):
    if not is_valid_table(table):
        raise Exception("Invalid table")

    sql = f"SELECT * FROM {table} WHERE id = %s"
    result = execute_query(sql, (row_id,), fetch=True)
    return result[0] if result else None


def insert_row(table, data: dict):
    if not is_valid_table(table):
        raise Exception("Invalid table")
    
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["%s"] * len(data))

    sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    execute_query(sql, tuple(data.values()))


def update_row(table, row_id, data: dict):
    if not is_valid_table(table):
        raise Exception("Invalid table")
    
    set_clause = ", ".join([f"{k} = %s" for k in data.keys()])

    sql = f"UPDATE {table} SET {set_clause} WHERE id = %s"
    execute_query(sql, tuple(data.values()) + (row_id,))


def delete_row(table, row_id):
    if not is_valid_table(table):
        raise Exception("Invalid table")
    
    sql = f"DELETE FROM {table} WHERE id = %s"
    execute_query(sql, (row_id,))
