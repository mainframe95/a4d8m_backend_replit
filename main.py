from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware import Middleware
from tortoise import Tortoise

from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from pydantic import BaseModel
from common.dependencies import get_current_user
import time
from starlette.middleware.base import BaseHTTPMiddleware

from account.route import api as account_api, get_current_user
from administration.api import api as admin_api


class Message(BaseModel):
    message: str

app = FastAPI()

# class Mid(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         start_time = time.time()
#         # print('request', vars(request))
#         # print('request', type(request.headers))
#         print('request mid', type(request.headers._list))

#         for el in dict(request.headers._list):
#             print(dict(request.headers._list)[el])
#         response = await call_next(request)
#         process_time = time.time() - start_time
#         # print(process_time)
#         return response
    

# app.add_middleware(Mid)
# dependencies=[Depends(get_current_user)]
app.include_router(admin_api)
app.include_router(account_api, )

@app.get('/')
async def read_root(request: Request):
    # print('request app', vars(request._headers))
    return {"Hello": "World"}

# @app.post('/todo', response_model=Todo_Pydantic)
# async def create(todo: TodoIn_Pydantic):
#     obj = await Todo.create(**todo.dict(exclude_unset=True))
#     return await Todo_Pydantic.from_tortoise_orm(obj)

# @app.get('/todo/{id}', response_model=Todo_Pydantic, responses={404: {"model": HTTPNotFoundError}})
# async def get_one(id: int):
#     return await Todo_Pydantic.from_queryset_single(Todo.get(id=id))

# @app.put("/todo/{id}", response_model=Todo_Pydantic, responses={404: {"model": HTTPNotFoundError}})
# async def update(id: int, todo: TodoIn_Pydantic):
#     await Todo.filter(id=id).update(**todo.dict(exclude_unset=True))
#     return await Todo_Pydantic.from_queryset_single(Todo.get(id=id))

# @app.delete("/todo/{id}", response_model=Message, responses={404: {"model": HTTPNotFoundError}})
# async def delete(id: int):
#     delete_obj = await Todo.filter(id=id).delete()
#     if not delete_obj:
#         raise HTTPException(status_code=404, detail="This todo is not found.")
#     return Message(message="Succesfully Deleted")

TORTOISE_ORM = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.sqlite',
            'credentials': {
                'file_path': 'db.sqlite3',
                'journal_mode': 'WAL',
            },
        },
    },
    'apps': {
        'models': {
            'models': ['models', "aerich.models"],
            'default_connection': 'default',
        },
    },
}


@app.on_event('startup')
async def startup():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()

@app.on_event('shutdown')
async def shutdown():
    await Tortoise.close_connections()

# register_tortoise(
#     app,
#     # config={''}
#     db_url='sqlite://db.sqlite',
#     modules={'models': ['models']},
#     generate_schemas=True,
#     add_exception_handlers=True,
# )

