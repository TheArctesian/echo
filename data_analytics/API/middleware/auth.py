from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
import jwt
import os

security = HTTPBearer()

async def verify_token(request: Request):
    try:
        auth = await security(request)
        token = auth.credentials
        payload = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['HS256'])
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authentication")
