from pydantic import BaseModel
from typing import Annotated, List, Optional

class UserBase(BaseModel):
    username:str
    email:str
    name:str
    age:int
class UserRead(BaseModel):
    id:int
    username:str
    email:str
    name:str
    age:int

class UpdateEmail(BaseModel):
    email:str
