
from fastapi import APIRouter, status, Depends, HTTPException
from .schema import *
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .services import created_admin, login
from jose import jwt, JWTError
from models import Admin

from common.utils import ALGORITHM, SECRET_KEY


api = APIRouter(tags=["Administrator"], prefix="/admin")
security = HTTPBearer()


@api.get("/")
def read_root():
    return {"Admin": "Tration"}

@api.post('/auth/login', response_model=TokenOut)
async def admin_login(data: AdminCredential):
    return await login(data)


@api.post('/create-admin', response_model=AdminOut)
async def create_admin(data: AdminCreate):
    return await created_admin(data)


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
        print('payload', payload)
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
        # token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await Admin.get(email=email)
    if user is None:
        raise credentials_exception
    return user



@api.get('/who-am-i', response_model=CurrentUser)
async def who_am_i(user: CurrentUser = Depends(get_current_user)):
    return user