import re
import secrets
import string

from fastapi import HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DoesNotExist

from .schema import AdminCreate, AdminCredential
from models import Admin
from common.utils import PWD_CTX, hash_password, create_access_token





def generate_random_string(length):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(length))


def verify_password(plain_password, hashed_password):
    return PWD_CTX.verify(plain_password, hashed_password)


def get_password_hash(password):
    return PWD_CTX.hash(password)


def extract_username(email):
    pattern = r'^[^@]+'
    match = re.search(pattern, email)
    if match:
        return match.group(0)
    else:
        return None



# function to create admin
async def created_admin(data: AdminCreate):
    try:
        await Admin.get(email=data.email)
        raise HTTPException(status_code=400, detail="Email already exists")
    except DoesNotExist: 
        admin = Admin(**data.dict())
        admin.pwd = hash_password(generate_random_string(12))
        admin.username = extract_username(data.email)
        await admin.save()
        return admin
    

async def login(data: AdminCredential):
    try:
        admin = await Admin.get(email = data.email)
        if not PWD_CTX.verify(data.password , admin.pwd):
            raise HTTPException(status_code=401, detail="Email or password invalid.")
        return {'token': create_access_token({'email': admin.email, 'id': str(admin.id) })}
    except Exception as e:
        print (e)
        raise HTTPException(status_code=401, detail="Email or password invalid.")



# Define an OAuth2 password flow for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Define a security scheme for bearer token authentication
bearer_scheme = HTTPBearer()

# A list of authorized bearer tokens (in practice, this would be stored in a database or other secure storage)
AUTHORIZED_TOKENS = [
    "some-secret-token-1",
    "another-secret-token-2",
]

# Define a function to check if a given token is authorized
async def is_token_authorized(token: str) -> bool:
    return token in AUTHORIZED_TOKENS

# Define a dependency that checks the authorization header and returns the bearer token
async def get_bearer_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    if credentials.scheme != "Bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication scheme")
    return credentials.credentials

# Define an endpoint that requires bearer token authentication
# @app.get("/protected")
# async def protected_endpoint(token: str = Depends(get_bearer_token)):
#     if not await is_token_authorized(token):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
#     return {"message": "You are authorized!"}



