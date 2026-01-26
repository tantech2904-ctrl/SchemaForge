from db.executor import execute_query

def list_tables():
    rows = execute_query("SHOW TABLES", fetch=True)
    return [list(row.values())[0] for row in rows]

def list_columns(table: str):
    return execute_query(f"DESCRIBE `{table}`", fetch=True)
