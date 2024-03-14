from sqlalchemy import Boolean, Column, ForeignKey, Integer, String ,Float
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_name = Column(String, unique=True)
    hashed_password = Column(String)
    name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    administration_role = Column(Boolean)

    # One-to-one relationship with Profile
    profile = relationship("Profile", uselist=False, back_populates="user")

class Profile(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    steam_userName = Column(String)
    steam_password = Column(String)

    # Define the back reference to User
    user = relationship("User", back_populates="profile")
    
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
    user_name=Column(String)
    steam_id=Column(String)
    