
import phonenumbers
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timezone, timedelta

SECRET_KEY = "votre-secret-key-secrete"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3600

PWD_CTX = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def phone_number_validator(phonenumber: str) -> dict({"tel": str, "is_valid": bool, "is_possible_number": bool}):
    num_parse = phonenumbers.parse(phonenumber)

    data = {
        "tel": '+' + str(num_parse.country_code) + '' + str(num_parse.national_number),
        "is_valid": phonenumbers.is_valid_number(num_parse),
        "is_possible_number": phonenumbers.is_possible_number(num_parse)
    }
    return data


def hash_password(password: str) -> str:
    return  PWD_CTX.hash(password)


def create_access_token(data: dict):
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt