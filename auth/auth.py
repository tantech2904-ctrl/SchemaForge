from db.executor import execute_query
from auth.security import hash_password, verify_password, create_token

def register_user(username, password, role="user"):
    hashed = hash_password(password)
    query = """
    INSERT INTO users (username, password_hash, role)
    VALUES (%s, %s, %s)
    """
    execute_query(query, (username, hashed, role))
    return {"message": "User registered"}

def login_user(username, password):
    query = "SELECT * FROM users WHERE username=%s"
    user = execute_query(query, (username,), fetch=True)

    if not user:
        return None

    user = user[0]
    if not verify_password(password, user["password_hash"]):
        return None

    token = create_token({
        "username": user["username"],
        "role": user["role"]
    })

    return {"token": token, "role": user["role"]}
