
from jose import JWTError, jwt

import random
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel


from common.utils import phone_number_validator
from common.customException import CodeExpiredException
from .schema import AccountInfo
from models import Account


SECRET_KEY = "votre-secret-key-secrete"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3600

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

async def register_by_phone(number: str) -> AccountInfo | bool:
    try:
        num_parse = await phone_number_validator(number)
        print('----g', num_parse)
        if num_parse["is_valid"] or num_parse["is_possible_number"]:
            # Update old auth code
            account = await Account.get_or_none(phonenumber = num_parse['tel'])
            if account:
                account.auth_code = str(random.random())[2:7]
                account.auth_expiration_date = datetime.now(tz=timezone.utc) + timedelta(hours=3)
                await account.save()
                return True
            else:
                # Account insert new user
                await Account.create(
                    phonenumber = num_parse["tel"],
                    auth_code = str(random.random())[2:7],
                    auth_expiration_date = datetime.now(tz=timezone.utc) + timedelta(hours=3)
                    )
                return True
    except Exception as e:
        print('error dans register', e)
        return False


async def account_info() -> list[AccountInfo]:
    return await Account.all()


async def auth_code(phonenumber: str) -> str:
    print('phonenumber', phonenumber)
    try:
        num_parse = await phone_number_validator(phonenumber)
        data = await Account.get(phonenumber = num_parse["tel"])
        if (data.auth_expiration_date.date() < datetime.now().date()):
            # envoi d'une exception expiered
            raise CodeExpiredException()
        return data.auth_code
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= 'Phone number not found'
        )



def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def validate_auth_code(phonenumber: str, user_code: str):
    num_parse = await phone_number_validator(phonenumber)
    code = await auth_code(num_parse['tel'])
    if code == user_code:
        account = await Account.get(phonenumber = num_parse["tel"])
        # creatation of jwt tokent
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"phonenumber": account.phonenumber}, expires_delta=access_token_expires
        )
        return access_token
    else:
        raise  HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect user information",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def active_user():
    pass


# class Token(BaseModel):
#     access_token: str
#     token_type: str


# class TokenData(BaseModel):
#     username: str | None = None


# class User(BaseModel):
#     username: str
#     email: str | None = None
#     full_name: str | None = None
#     disabled: bool | None = None


# class UserInDB(User):
#     hashed_password: str


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         print('payload', payload)
#         username: str = payload.get("phonenumber")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = Account.get(phonenumber=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user



# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user

# from datetime import datetime, timedelta
# from fastapi import Depends, FastAPI, HTTPException
# from passlib.context import CryptContext
# from tortoise.contrib.fastapi import register_tortoise

# from .models import User

# app = FastAPI()



# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# async def authenticate_user(username: str, password: str):
#     user = await User.get(username=username)

#     if not user:
#         return False

#     if not pwd_context.verify(password, user.password):
#         return False

#     return user


# @app.post("/token")
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = await authenticate_user(form_data.username, form_data.password)

#     if not user:
#         raise HTTPException(status_code=400, detail="Identifiants invalides")

#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username},
#         expires_delta=access_token_expires
#     )

#     return {"access_token": access_token, "token_type": "bearer"}

# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise HTTPException(status_code=401, detail="Token invalide")
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Token invalide")

#     user = await Account.get(username=username)

#     if not user:
#         raise HTTPException(status_code=401, detail="Token invalide")

#     return user



# register_tortoise(
#     app,
#     db_url="sqlite://db.sqlite3",
#     modules={"models": ["app.models"]},
#     generate_schemas=True
# )

