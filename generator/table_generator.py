from db.executor import execute_query

ALLOWED_TYPES = {
    "INT",
    "VARCHAR(255)",
    "VARCHAR(100)",
    "TEXT",
    "DATE",
    "FLOAT",
    "BOOLEAN"
}

def generate_create_table_sql(table_name, columns):
    column_definitions = []

    for col in columns:
        col_name = col["name"]
        col_type = col["type"]

        if col_type not in ALLOWED_TYPES:
            raise ValueError(f"Invalid column type: {col_type}")

        line = f"{col_name} {col_type}"

        if col.get("primary"):
            line += " PRIMARY KEY"

        if col.get("auto_increment"):
            line += " AUTO_INCREMENT"

        column_definitions.append(line)

    columns_sql = ", ".join(column_definitions)
    sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql})"

    return sql


def create_table(table_name, columns):
    sql = generate_create_table_sql(table_name, columns)
    execute_query(sql)
