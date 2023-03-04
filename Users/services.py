
# from sqlalchemy.orm import Session
# from core.databases import engine

from . import schemas


def get_user( user_id: int):
    # return db.query(models.User)
    return


def get_all_user():
    # return db.query(models.User)
    return


def create_user(user: schemas.UserCreate):
    # db = Session(engine)
    # fake_hashed_password = user.password + "notreallyhashed"
    # db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    # db.add(db_user)
    # db.commit()
    # # db.refresh(db_user)
    # print("\n", db_user, "\n")
    # return db_user
    return
