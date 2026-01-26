from fastapi import APIRouter, Depends
from core.dependencies import get_current_user
from core.permissions import can_read
from services.metadata import list_tables, list_columns

router = APIRouter(prefix="/metadata", tags=["Metadata"])

@router.get("/tables")
def get_tables(user=Depends(get_current_user)):
    can_read(user["role"])
    return {"tables": list_tables()}

@router.get("/tables/{table}/columns")
def get_columns(table: str, user=Depends(get_current_user)):
    can_read(user["role"])
    return {"columns": list_columns(table)}
