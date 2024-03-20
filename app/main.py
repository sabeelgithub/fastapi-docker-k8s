from fastapi import FastAPI,HTTPException,Depends,status
from typing import List,Annotated
from . import models
from app.database import engine,get_db
from sqlalchemy.orm import Session
from app.schemas import UserBase,ReadEmail

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session,Depends(get_db)]

@app.post("/create-user")
async def create_user(user:UserBase,db:db_dependency):
    """
    This endpoint is responsible for creating users
    """
    db_user = models.User(username=user.username,email=user.email,name=user.name,age=user.age)
    db.add(db_user)
    db.commit()
    return {"message":"User created successfully","status":status.HTTP_200_OK}

@app.get("/read-users",response_model=List[UserBase])
async def read_users(db:db_dependency):
    """
    This endpoint is responsible for reading all users
    """
    users = db.query(models.User).all()
    return users

@app.get("/read-user-by-id",response_model=UserBase)
async def read_user_by_id(db:db_dependency,id:int):
    """
    This endpoint is responsible for reading single user by id
    """
    user = db.query(models.User).get(id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="There is no matching user")
    return user

@app.get("/read-user-by-email",response_model=List[UserBase])
async def read_user_by_email(db:db_dependency,email:str):
    """
    This endpoint is responsible for reading single user by email
    """
    user = db.query(models.User).filter_by(email=email).all()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="There is no matching user")
    return user







