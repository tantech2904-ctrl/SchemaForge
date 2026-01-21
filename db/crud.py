from db.executor import execute_query
from db.metadata import is_valid_table

def get_all_rows(table: str):
    if not is_valid_table(table):
        return {"error": "Invalid table"}

    query = f"SELECT * FROM `{table}`"
    return execute_query(query, fetch=True)


def insert_row(table: str, data: dict):
    if not is_valid_table(table):
        return {"error": "Invalid table"}

    columns = ", ".join(f"`{k}`" for k in data.keys())
    placeholders = ", ".join(["%s"] * len(data))
    values = tuple(data.values())

    query = f"INSERT INTO `{table}` ({columns}) VALUES ({placeholders})"
    execute_query(query, values)
    return {"message": "Row inserted"}


def update_row(table: str, row_id: int, data: dict):
    if not is_valid_table(table):
        return {"error": "Invalid table"}

    set_clause = ", ".join(f"`{k}`=%s" for k in data.keys())
    values = tuple(data.values()) + (row_id,)

    query = f"UPDATE `{table}` SET {set_clause} WHERE id=%s"
    execute_query(query, values)
    return {"message": "Row updated"}


def delete_row(table: str, row_id: int):
    if not is_valid_table(table):
        return {"error": "Invalid table"}

    query = f"DELETE FROM `{table}` WHERE id=%s"
    execute_query(query, (row_id,))
    return {"message": "Row deleted"}
