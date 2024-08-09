from sqlalchemy import Boolean, Column, ForeignKey, Integer, String ,Float ,Enum
from sqlalchemy.orm import relationship
from app.database import Base
from enums.user_roles import UserRole
from enums.order_status import order_status
    
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    role = Column(Enum(UserRole))

    # One-to-one relationship with Profile
    profile = relationship("Profile", uselist=False, back_populates="user")
    # one-to-many relationship with orders
    orders = relationship("Order", back_populates="user")


class Profile(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, index=True)
    steam_username = Column(String)
    steam_password = Column(String)

    # Define the back reference to User
    user = relationship("User", back_populates="profile")
    
class Game(Base):
    __tablename__='games'
    id = Column(Integer, primary_key=True, index=True)
    name=Column(String, index=True)
    author=Column(String)
    steam_id=Column(String,unique=True)
    price=Column(Float)
    
    # One-to-one relationship with Order
    order=relationship("Order",uselist=False,back_populates="game")
class Order(Base):
    __tablename__='orders'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    game_id=Column(Integer,ForeignKey('games.id'))
    status=Column(Enum(order_status),default=order_status.PREPARATION)
    # One-to-one relationship with Game
    game=relationship("Game",back_populates="order")
    #many-to-one relationship with users
    user = relationship("User", back_populates="orders")
    