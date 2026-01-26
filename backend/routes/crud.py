from fastapi import APIRouter, Depends
from core.dependencies import get_current_user
from core.permissions import can_write,can_read
from schemas.crud import InsertRequest, UpdateRequest, DeleteRequest, SelectRequest
from services.crud import insert_row, update_row, delete_row, select_rows



router = APIRouter(prefix="/crud", tags=["CRUD"])

@router.post("/insert")
def insert(data: InsertRequest, user=Depends(get_current_user)):
    can_write(user["role"])
    insert_row(data.table, data.data)
    return {"status": "inserted"}

@router.put("/update")
def update(data: UpdateRequest, user=Depends(get_current_user)):
    can_write(user["role"])
    update_row(data.table, data.data, data.where)
    return {"status": "updated"}

@router.delete("/delete")
def delete(data: DeleteRequest, user=Depends(get_current_user)):
    can_write(user["role"])
    delete_row(data.table, data.where)
    return {"status": "deleted"}

@router.post("/select")
def select(data: SelectRequest, user=Depends(get_current_user)):
    can_read(user["role"])
    rows = select_rows(
        data.table,
        data.columns,
        data.where,
        data.limit,
        data.offset
    )
    return {"rows": rows}