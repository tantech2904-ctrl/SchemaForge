from fastapi import APIRouter, Depends, HTTPException
from db.crud import get_all_rows, insert_row, update_row, delete_row
from auth.dependencies import get_current_user
from auth.permissions import has_permission
from schemas.crud_schema import CRUDPayload
from schemas.response_schema import APIResponse
from db.audit import log_audit

router = APIRouter(prefix="/crud", tags=["CRUD"])

@router.get("/{table}")
def read_table(table: str, user=Depends(get_current_user)):
    if not has_permission(user["role"], table, "read"):
        raise HTTPException(status_code=403, detail="Read not allowed")

    return get_all_rows(table)

@router.post("/{table}")
def create_row(
    table: str,
    payload: CRUDPayload,
    user=Depends(get_current_user)
):
    if not has_permission(user["role"], table, "create"):
        raise HTTPException(status_code=403, detail="Create not allowed")

    result = insert_row(table, payload.data)

    log_audit(
        user=user,
        action="CREATE",
        table=table,
        row_id=result.get("id"),
        payload=payload.data
    )

    return APIResponse(True, "Row created", result)



@router.put("/{table}/{row_id}")
def update_row_route(
    table: str,
    row_id: int,
    payload: CRUDPayload,
    user=Depends(get_current_user)
):
    if not has_permission(user["role"], table, "update"):
        raise HTTPException(status_code=403, detail="Update not allowed")

    update_row(table, row_id, payload.data)

    log_audit(
        user=user,
        action="UPDATE",
        table=table,
        row_id=row_id,
        payload=payload.data
    )

    return APIResponse(True, "Row updated")



@router.delete("/{table}/{row_id}")
def remove_row(
    table: str,
    row_id: int,
    user=Depends(get_current_user)
):
    if not has_permission(user["role"], table, "delete"):
        raise HTTPException(status_code=403, detail="Delete not allowed")

    delete_row(table, row_id)

    log_audit(
        user=user,
        action="DELETE",
        table=table,
        row_id=row_id
    )

    return APIResponse(True, "Row deleted")


