from pydantic import BaseModel
from enums.user_roles import UserRole
from enums.order_status import order_status

class UserBase(BaseModel):
    username:str
    name:str
    last_name:str
    phone_number:str
    
class UserProfile(UserBase):
    steam_username:str
    steam_password:str   
    
class UserIn(UserProfile):
    password:str  
    pass
class UserOut(UserProfile):
    id:int
    role:UserRole
    class Config:
        from_attributes=True
        
        
class AdminIn(UserBase):
    password:str    
class AdminOut(UserBase):
    id:int
    role:UserRole
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
    id:int
    class Confing:
        from_attributes=True
        
        
class Order(BaseModel):
    game_id:int
class OrderIn(Order):
    pass    
class OrderOut(Order):
    user_id:int
    status:order_status
    id:int
    class Confing:
        from_attributes=True
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    role: UserRole | None = None
    id: int