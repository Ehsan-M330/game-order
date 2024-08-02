from pydantic import BaseModel
from enums.user_roles import UserRole


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
        from_attributes=True
        
        
class AdminIn(UserBase):
    password:str    
class AdminOut(UserBase):
    class Config:
        from_attributes=True
        

    
class GameBase(BaseModel):
    name:str
    author:str
    steam_id:str
    price:float
class GameIn(GameBase):
    pass
class GameOut(GameBase):
    class Confing:
        from_attributes=True
        
        
class Order(BaseModel):
    user_id:str
    steam_id:str
    
    
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    role:UserRole | None = None