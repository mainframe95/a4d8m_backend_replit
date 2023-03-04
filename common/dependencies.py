
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, status, Depends
from jose import JWTError, jwt

from models import Account

SECRET_KEY = "votre-secret-key-secrete"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


security = HTTPBearer()

async def get_current_user(security: HTTPBearer = Depends(security)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    credentials: HTTPAuthorizationCredentials = security
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("phonenumber")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await Account.get(phonenumber=username)
    if user is None:
        raise credentials_exception
    return user

