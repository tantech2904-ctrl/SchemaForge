from db.executor import execute_query
import json

def log_audit(
    user: dict,
    action: str,
    table: str = None,
    row_id: int = None,
    payload: dict = None
):
    execute_query(
        """
        INSERT INTO audit_logs (username, role, action, table_name, row_id, payload)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        params=(
            user["username"],
            user["role"],
            action,
            table,
            row_id,
            json.dumps(payload) if payload else None
        ),
        commit=True
    )
