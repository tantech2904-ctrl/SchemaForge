from fastapi import HTTPException

def can_write(role: str):
    if role not in ("admin",):
        raise HTTPException(status_code=403, detail="Write access denied")

def can_read(role: str):
    if role not in ("admin", "user"):
        raise HTTPException(status_code=403, detail="Read access denied")
