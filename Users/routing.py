
from fastapi import APIRouter

from .services import get_all_user, create_user
from .schemas import UserCreate

api = APIRouter(prefix="")

@api.get("/USER")
def read_root():
    return {"Hello": "World"}


@api.post('/register')
async def account_register(account):
    return


@api.get('/all')
def get_all():
    return get_all_user()


@api.post('/user', )
def create(user: UserCreate):
    g = create_user(user)
    pass

