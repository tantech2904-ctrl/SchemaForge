from fastapi import APIRouter, HTTPException, Depends
from schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from core.security import verify_password, create_access_token, hash_password
from core.dependencies import require_admin
from db.executor import execute_query

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):
    user = execute_query(
        "SELECT * FROM users WHERE username=%s AND is_active=1",
        (data.username,),
        fetchone=True
    )

    if not user or not verify_password(data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "user_id": user["id"],
        "role": user["role"]
    })

    return {"access_token": token}


@router.post("/register")
def register_user(data: RegisterRequest):
    existing = execute_query(
        "SELECT id FROM users WHERE username=%s OR email=%s",
        (data.username, data.email),
        fetchone=True
    )

    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    execute_query(
        """
        INSERT INTO users (username, email, password_hash, role)
        VALUES (%s, %s, %s, 'user')
        """,
        (data.username, data.email, hash_password(data.password))
    )

    return {"message": "User registered successfully"}
