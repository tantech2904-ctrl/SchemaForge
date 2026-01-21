from fastapi import APIRouter
from auth.auth import register_user, login_user

router = APIRouter(prefix="/auth")

@router.post("/register")
def register(username: str, password: str, role: str = "user"):
    return register_user(username, password, role)

@router.post("/login")
def login(username: str, password: str):
    result = login_user(username, password)
    if not result:
        return {"error": "Invalid credentials"}
    return result
