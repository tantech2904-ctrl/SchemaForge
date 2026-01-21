from db.metadata import get_accessible_tables

@router.get("/tables")
def list_tables(user=Depends(get_current_user)):
    return get_accessible_tables(user["role"])
