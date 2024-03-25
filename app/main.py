from fastapi import FastAPI,HTTPException,Depends,status
from sqlalchemy import func
from typing import List,Annotated
from . import models
from app.database import engine,get_db
from sqlalchemy.orm import Session
from app.schemas import UserBase,UserRead,UpdateEmail

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

@app.get("/read-users",response_model=List[UserRead])
async def read_users(db:db_dependency):
    """
    This endpoint is responsible for reading all users
    """
    users = db.query(models.User).all()
    return users

@app.get("/read-user-by-id",response_model=UserRead)
async def read_user_by_id(db:db_dependency,id:int):
    """
    This endpoint is responsible for reading single user by id
    """
    user = db.query(models.User).get(id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="There is no matching user")
    return user

@app.get("/read-user-by-email",response_model=List[UserRead])
async def read_user_by_email(db:db_dependency,email:str):
    """
    This endpoint is responsible for reading single user by email
    """
    user = db.query(models.User).filter_by(email=email).all()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="There is no matching user")
    return user

@app.get("/read-user-by-username",response_model=List[UserRead])
async def read_user_by_username(db:db_dependency,username:str):
    """
    This endpoint is responsible for reading single user by username
    """
    user = db.query(models.User).filter_by(username=username).all()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="There is no matching user")
    return user

@app.patch("/update-user")
async def update_user(db:db_dependency,id:int,request_data:UpdateEmail):
    """
    This endpoint is responsible for updating users
    """
    user = db.query(models.User).get(id)
    print(user,'user')
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="There is no matching user")
    
    user.email = request_data.email
    db.commit()
    return {"message":"User's email updated successfully","status":status.HTTP_200_OK}

@app.delete("/delete-user")
async def delete_user(db:db_dependency,id:int):
    """
    This endpoint is responsible for deleting user 
    """
    user = db.query(models.User).get(id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="There is no matching user")
    
    db.delete(user)
    db.commit()
    return {"message":"User deleted successfully","status":status.HTTP_200_OK}







