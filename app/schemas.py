from pydantic import BaseModel
from enums.user_roles import UserRole
from enums.order_status import order_status
from typing import List
from datetime import datetime


class UserBase(BaseModel):
    username: str
    name: str
    last_name: str
    phone_number: str


class UserProfile(UserBase):
    steam_username: str
    steam_password: str


class UserIn(UserProfile):
    password: str
    pass


class UserOut(UserProfile):
    id: int
    role: UserRole

    class Config:
        from_attributes = True


class UserOut_withPassword(UserOut):
    hashed_password: str


class AdminIn(UserBase):
    password: str


class AdminOut(UserBase):
    id: int
    role: UserRole

    class Config:
        from_attributes = True


class GameBase(BaseModel):
    name: str
    author: str
    steam_id: str
    price: float


class GameIn(GameBase):
    pass


class GameOut(GameBase):
    id: int

    class Config:
        from_attributes = True


class GamesListResponse(BaseModel):
    data: List[GameOut]
    total_data: int
    total_pages: int
    message: str | None = (
        None  # Optional, only used when there are no games or an error occurs
    )


class Order(BaseModel):
    game_id: int


class OrderIn(Order):
    pass


class OrderOut(Order):
    user_id: int
    status: order_status
    id: int
    order_date: datetime

    class Confing:
        from_attributes = True


class OrdersListResponse(BaseModel):
    data: List[OrderOut]
    total_data: int
    total_pages: int
    message: str | None = (
        None  # Optional, only used when there are no orders or an error occurs
    )


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    role: UserRole | None = None
    id: int
