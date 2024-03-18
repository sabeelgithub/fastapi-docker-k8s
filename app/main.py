from fastapi import FastAPI,HTTPException,Depends,status
from typing import List,Annotated
from . import models
from app.database import engine,get_db
from sqlalchemy.orm import Session
from app.schemas import UserBase

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session,Depends(get_db)]

@app.post("/create-user")
async def create_user(user:UserBase,db:db_dependency):
    db_user = models.User(name=user.name,age=user.age)
    db.add(db_user)
    db.commit()
    return {"message":"User created successfully","status":status.HTTP_200_OK}

@app.get("/read-users",response_model=List[UserBase])
async def read_users(db:db_dependency):
    users = db.query(models.User).all()
    return users







