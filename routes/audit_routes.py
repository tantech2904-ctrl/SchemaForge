from fastapi import APIRouter, Depends
from db.executor import execute_query
from auth.dependencies import get_current_user

router = APIRouter(prefix="/audit", tags=["Audit"])

@router.get("/")
def get_logs(user=Depends(get_current_user)):
    if user["role"] != "admin":
        return []

    return execute_query(
        "SELECT * FROM audit_logs ORDER BY timestamp DESC",
        fetch=True
    )
