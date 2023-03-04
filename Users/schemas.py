
from pydantic import BaseModel

class User(BaseModel):
    id: int
    is_active: bool
    # items: list[Item] = []

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: str
    password: str

