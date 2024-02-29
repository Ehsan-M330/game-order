from fastapi import FastAPI
from pydantic import BaseModel,constr
from typing import Annotated

#models
class User(BaseModel):
    name:str
    last_name:str
    phone_number:str
    steam_usreName:str
    steam_password:str

class Admin(BaseModel):
    user_name:str
    password:str

class Game(BaseModel):
    name:str
    author:str
    steam_id:str
    price:float

app = FastAPI()

@app.post('/admin/init')
async def add_admin(admin:Admin):
    return admin

@app.post('/user/init')
async def add_user(user:User):
    return user



