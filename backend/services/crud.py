from db.executor import execute_query

def insert_row(table: str, data: dict):
    cols = ", ".join(f"`{k}`" for k in data)
    placeholders = ", ".join(["%s"] * len(data))
    sql = f"INSERT INTO `{table}` ({cols}) VALUES ({placeholders})"
    execute_query(sql, tuple(data.values()))

def update_row(table: str, data: dict, where: dict):
    set_clause = ", ".join(f"`{k}`=%s" for k in data)
    where_clause = " AND ".join(f"`{k}`=%s" for k in where)
    sql = f"UPDATE `{table}` SET {set_clause} WHERE {where_clause}"
    execute_query(sql, tuple(data.values()) + tuple(where.values()))

def delete_row(table: str, where: dict):
    where_clause = " AND ".join(f"`{k}`=%s" for k in where)
    sql = f"DELETE FROM `{table}` WHERE {where_clause}"
    execute_query(sql, tuple(where.values()))

def select_rows(
    table: str,
    columns: list[str] | None,
    where: dict | None,
    limit: int,
    offset: int
):
    cols = ", ".join(f"`{c}`" for c in columns) if columns else "*"

    sql = f"SELECT {cols} FROM `{table}`"
    params = []

    if where:
        conditions = []
        for k, v in where.items():
            conditions.append(f"`{k}`=%s")
            params.append(v)
        sql += " WHERE " + " AND ".join(conditions)

    sql += " LIMIT %s OFFSET %s"
    params.extend([limit, offset])

    return execute_query(sql, tuple(params), fetch=True)