from pydantic import BaseModel

class UserBase(BaseModel):
    user_id:str
    name:str
    last_name:str
    phone_number:str
    steam_userName:str
    steam_password:str
    
class UserCreate(UserBase):
    password:str
        
class User(UserBase):
    id:int
    
    class Config:
        orm_mode=True
    
class Admin(BaseModel):
    user_id:str
    password:str

class Game(BaseModel):
    name:str
    author:str
    steam_id:int
    price:float
class Order(BaseModel):
    user_id:str
    steam_id:str
    