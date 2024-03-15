from pydantic import BaseModel

class UserBase(BaseModel):
    user_name:str
    name:str
    last_name:str
    phone_number:str
    
class UserProfile(UserBase):
    steam_userName:str
    steam_password:str   
class UserIn(UserProfile):
    password:str  
    pass
class UserOut(UserProfile):
    class Config:
        orm_mode=True
        
        
class AdminIn(UserBase):
    password:str    
class AdminOut(UserBase):
    class Config:
        orm_mode=True
        

    
class GameBase(BaseModel):
    name:str
    author:str
    steam_id:str
    price:float
class GameIn(GameBase):
    pass
class GameOut(GameBase):
    class Confing:
        orm_mode=True
        
        
class Order(BaseModel):
    user_id:str
    steam_id:str
    