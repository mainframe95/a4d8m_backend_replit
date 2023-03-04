from pydantic import BaseModel, EmailStr


class AdminCreate(BaseModel):
    email: EmailStr
    access: str
    firstname: str
    lastname: str


class AdminOut(BaseModel):
    username: str
    email: EmailStr
    access: str = None
    firstname: str = None
    lastname: str = None


class AdminCredential(BaseModel):
    email: EmailStr
    password: str


class CurrentUser(BaseModel):
    email: str


class TokenOut(BaseModel):
    token: str

