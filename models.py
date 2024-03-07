from sqlalchemy import Boolean, Column, ForeignKey, Integer, String ,Float
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__='users'
    user_id=Column(Integer,primary_key=True)
    hashed_password=Column(String)
    name=Column(String)
    last_name=Column(String)
    phone_number=Column(Integer,unique=True)
    steam_userName=Column(String)
    steam_password=Column(String)
    
class Admin(Base):
    __tablename__='admin'
    user_id=Column(Integer,primary_key=True)
    hashed_password=Column(String)
    
class Game(Base):
    __tablename__='game'
    name=Column(String)
    author=Column(String)
    steam_id=Column(Integer,unique=True)
    price=Column(Float)
    
class Order(Base):
    __tablename__='order'
    user_id=Column(String)
    steam_id=Column(String)
    