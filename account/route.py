from fastapi import APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .services import *
from .schema import AccountByPhone, AccountInfo, CodeVerify

api = APIRouter(prefix="", tags=["Accounts"])

@api.get('/info')
async def info() -> list[AccountInfo]:
    return await account_info()

# , response_model=Todo_Pydantic), response_model=AccountInfo
@api.post('/resgister')
async def phone_register(data: AccountByPhone) -> AccountInfo | bool:
    return await register_by_phone(data.number)

@api.get('/{phonenumber}/auth-code')
async def get_auth_code(phonenumber: str) -> str:
    return await auth_code(phonenumber)

@api.post('/{phonenumber}/code-verify')
async def code_verify(phonenumber: str, data: CodeVerify):
    return await validate_auth_code(phonenumber, data.code)

@api.get('active')
async def get_active_user():
    return active_user()

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
        print('payload', payload)
        username: str = payload.get("phonenumber")
        if username is None:
            raise credentials_exception
        # token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await Account.get(phonenumber=username)
    if user is None:
        raise credentials_exception
    return user




@api.get("/items/pop", dependencies=None)
async def read_items(current_user: AccountInfo = Depends(None)):
    return current_user
