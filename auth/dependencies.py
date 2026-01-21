from fastapi import Header, HTTPException
import jwt
from auth.security import SECRET_KEY, ALGORITHM

def get_current_user(authorization: str = Header(...)):
    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
