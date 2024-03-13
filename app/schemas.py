from pydantic import BaseModel
from typing import Annotated, List, Optional

class UserBase(BaseModel):
    name:str
    age:int
