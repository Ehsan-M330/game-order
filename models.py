from sqlalchemy import Boolean, Column, ForeignKey, Integer, String ,Float
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__='users'
    
    id=Column(Integer,primary_key=True)
    user_id=Column(String)
    hashed_password=Column(String)
    name=Column(String)
    last_name=Column(String)
    phone_number=Column(String)
    steam_userName=Column(String)
    steam_password=Column(String)
    
class Admin(Base):
    __tablename__='admin'
    id=Column(Integer,primary_key=True)
    user_id=Column(Integer)
    password=Column(String)
    
class Game(Base):
    __tablename__='game'
    id = Column(Integer, primary_key=True)
    name=Column(String)
    author=Column(String)
    steam_id=Column(Integer,unique=True)
    price=Column(Float)
    
class Order(Base):
    __tablename__='order'
    id = Column(Integer, primary_key=True)
    user_id=Column(String)
    steam_id=Column(String)
    