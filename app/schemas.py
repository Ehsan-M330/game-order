from pydantic import BaseModel, Field
from enums.user_roles import UserRole
from typing import List, Optional
from datetime import datetime
from tools.fake_data import (
    generate_fake_username,
    generate_fake_name,
    generate_fake_last_name,
    generate_fake_phone_number,
    generate_fake_price,
    generate_fake_id,
    generate_fake_game_name,
    generate_fake_date,
    generate_fake_steam_id,
    generate_fake_role,
    generate_fake_password,
    generate_fake_order_status,
)


class UserBase(BaseModel):
    username: str = Field(
        ...,
        examples=[generate_fake_username()],
        description="The user's unique username",
    )
    name: str = Field(
        ..., examples=[generate_fake_name()], description="The user's first name"
    )
    last_name: str = Field(
        ..., examples=[generate_fake_last_name()], description="The user's last name"
    )
    phone_number: str = Field(
        ...,
        examples=[generate_fake_phone_number()],
        description="The user's contact number",
    )


class UserProfile(UserBase):
    steam_username: str = Field(
        ...,
        examples=[generate_fake_username()],
        description="The user's Steam username",
    )
    steam_password: str = Field(
        ...,
        examples=[generate_fake_password()],
        description="The user's Steam password",
    )


class UserIn(UserProfile):
    password: str = Field(
        ..., examples=[generate_fake_password()], description="The user's password"
    )


class UserOut(UserProfile):
    id: int = Field(
        ..., examples=[generate_fake_id()], description="The user's unique identifier"
    )
    role: UserRole = Field(
        ..., examples=[generate_fake_role()], description="The user's role"
    )

    class Config:
        from_attributes = True


class UserOut_withPassword(UserOut):
    hashed_password: str = Field(
        ...,
        examples=[generate_fake_password()],
        description="The user's hashed password",
    )


class AdminIn(UserBase):
    password: str = Field(
        ..., examples=[generate_fake_password()], description="The admin's password"
    )


class AdminOut(UserBase):
    id: int = Field(
        ..., examples=[generate_fake_id()], description="The admin's unique identifier"
    )
    role: UserRole = Field(
        ..., examples=[generate_fake_role()], description="The admin's role"
    )

    class Config:
        from_attributes = True


class GameBase(BaseModel):
    name: str = Field(
        ..., examples=[generate_fake_game_name()], description="The game's name"
    )
    author: str = Field(
        ..., examples=[generate_fake_name()], description="The game's author"
    )
    steam_id: str = Field(
        ..., examples=[generate_fake_steam_id()], description="The game's Steam ID"
    )
    price: float = Field(
        ..., examples=[generate_fake_price()], description="The game's price"
    )


class GameIn(GameBase):
    pass


class GameOut(GameBase):
    id: int = Field(
        ..., examples=[generate_fake_id()], description="The game's unique identifier"
    )

    class Config:
        from_attributes = True


class GamesListResponse(BaseModel):
    data: List[GameOut] = Field(..., description="List of games")
    total_data: int = Field(..., description="Total number of games")
    total_pages: int = Field(..., description="Total number of pages")
    message: Optional[str] = Field(default=None, description="Optional message")


class Order(BaseModel):
    game_id: int = Field(
        ..., examples=[generate_fake_id()], description="The ID of the ordered game"
    )


class OrderIn(Order):
    pass


class OrderOut(Order):
    user_id: int = Field(
        ...,
        examples=[generate_fake_id()],
        description="The ID of the user who placed the order",
    )
    status: str = Field(
        ...,
        examples=[generate_fake_order_status()],
        description="The status of the order",
    )
    id: int = Field(
        ...,
        examples=[generate_fake_id()],
        description="The unique identifier of the order",
    )
    order_date: datetime = Field(
        ...,
        examples=[generate_fake_date()],
        description="The date the order was placed",
    )

    class Config:
        from_attributes = True


class OrdersListResponse(BaseModel):
    data: List[OrderOut] = Field(..., description="List of orders")
    total_data: int = Field(..., description="Total number of orders")
    total_pages: int = Field(..., description="Total number of pages")
    message: Optional[str] = Field(default=None, description="Optional message")


class Token(BaseModel):
    access_token: str = Field(..., description="The access token")
    token_type: str = Field(..., description="The type of the token")


class TokenData(BaseModel):
    username: Optional[str] = Field(
        None, examples=[generate_fake_username()], description="The username"
    )
    role: Optional[str] = Field(
        None, examples=[generate_fake_role()], description="The user's role"
    )
    id: int = Field(
        ..., examples=[generate_fake_id()], description="The unique identifier"
    )
