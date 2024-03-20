from sqlalchemy import Boolean,Column,ForeignKey,Integer,String
from app.database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer,primary_key=True,index=True)
    username = Column(String,index=True)
    email = Column(String,index=True)
    name = Column(String,index=True)
    age = Column(Integer,index=True)