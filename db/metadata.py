from db.executor import execute_query
from core.cache import set_cache,get_cache,clear_cache

# -------------------------------
# TABLE LISTING (CACHED)
# -------------------------------

def get_all_tables() -> list[str]:
    """
    Returns all tables in the current database (cached).
    """
    cached = get_cache("tables")
    if cached:
        return cached

    rows = execute_query("SHOW TABLES", fetch=True)
    tables = [list(row.values())[0] for row in rows]

    set_cache("tables", tables)
    return tables


def is_valid_table(table_name: str) -> bool:
    """
    Checks if a table exists in the database.
    """
    return table_name in get_all_tables()


# -------------------------------
# COLUMN METADATA (CACHED)
# -------------------------------

def get_table_columns(table_name: str) -> list[dict]:
    """
    Returns column metadata for a table (cached).
    """
    cache_key = f"columns:{table_name}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    query = f"DESCRIBE `{table_name}`"
    columns = execute_query(query, fetch=True)

    set_cache(cache_key, columns)
    return columns


# -------------------------------
# PERMISSION-AWARE TABLES (CACHED)
# -------------------------------

def get_accessible_tables(role: str) -> list[str]:
    """
    Returns tables the given role has ANY permission on.
    """
    cache_key = f"tables:{role}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    rows = execute_query(
        """
        SELECT DISTINCT table_name
        FROM permissions
        WHERE role = %s
        """,
        params=(role,),
        fetch=True
    )

    tables = [row["table_name"] for row in rows]

    set_cache(cache_key, tables)
    return tables

clear_cache()
