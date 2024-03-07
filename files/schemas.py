from pydantic import BaseModel

class User(BaseModel):
    user_id:str
    password:str
    name:str
    last_name:str
    phone_number:str
    steam_usreName:str
    steam_password:str

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
    