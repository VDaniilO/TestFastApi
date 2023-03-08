from typing import List

import uvicorn

from fastapi import FastAPI, Query, Depends
from fastapi_sqlalchemy import DBSessionMiddleware, db
from sqlalchemy.orm import Session
from schema import UserSchema
from model import User as UserModel
from model import SessionLocal

import os
from dotenv import load_dotenv


load_dotenv('.env')

app = FastAPI()


app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])


# определяем зависимость
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/create_user/', response_model=UserSchema)
async def post_user(users: UserSchema):
    db_user = UserModel(user_name=users.user_name, money=users.money)
    db.session.add(db_user)
    db.session.commit()
    return db_user


@app.get('/all_users/')
async def get_user():
    user = db.session.query(UserModel).all()
    return user


@app.put("/api/{u_name}")
def edit_person(u_name: str, users: UserSchema, amount: int,
                db: Session = Depends(get_db), action: List[str] = Query(["dept", "width"])):
    person = db.query(UserModel).filter(users.user_name == u_name).first()
    person.user_name = u_name

    if action == 'dept':
        person.money += amount
    if action == 'width':
        person.money -= amount

    db.commit()
    db.refresh(person)
    return person

# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
