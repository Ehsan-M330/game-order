from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
import hashlib  # type: ignore
from app import models, schemas
from enums.user_roles import UserRole
from app.auth.hashing import get_password_hash
from typing import List
from sqlalchemy.sql.elements import ColumnElement
from sqlalchemy.ext.declarative import DeclarativeMeta

# def hash_password(password: str) -> str:
#     """Hashes a password using SHA-256."""
#     hashed_password = hashlib.sha256(password.encode()).hexdigest()
#     return hashed_password


def get_user_byId(db: Session, id: int) -> schemas.UserOut_withPassword | None:
    return db.query(models.User).filter(models.User.id == id).first()


def get_user_byUsername(
    db: Session, username: str
) -> schemas.UserOut_withPassword | None:
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserIn):
    user.password = get_password_hash(user.password)

    db_user = models.User(
        name=user.name,
        last_name=user.last_name,
        username=user.username,
        hashed_password=user.password,
        phone_number=user.phone_number,
        role=UserRole.USER,
    )
    db.add(db_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is already in use.",
        )

    db_profile = models.Profile(
        steam_username=user.steam_username,
        steam_password=user.steam_password,
        user_id=db_user.id,
    )

    db.add(db_profile)
    db.commit()


def create_admin(db: Session, admin: schemas.AdminIn):
    admin.password = get_password_hash(admin.password)
    db_admin = models.User(
        name=admin.name,
        last_name=admin.last_name,
        username=admin.username,
        hashed_password=admin.password,
        phone_number=admin.phone_number,
        role=UserRole.ADMIN,
    )
    db.add(db_admin)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is already in use.",
        )


def create_game(db: Session, game: schemas.GameIn):
    db_game = models.Game(
        name=game.name, steam_id=game.steam_id, author=game.author, price=game.price
    )
    db.add(db_game)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Steam ID is already in use.",
        )


def check_order(db: Session, order: schemas.OrderIn):
    if db.query(models.Game).filter(models.Game.id == order.game_id).first():
        return True
    else:
        return False


def create_order(db: Session, order: schemas.OrderIn, user_id: int):
    db_order = models.Order(user_id=user_id, game_id=order.game_id)
    db.add(db_order)
    db.commit()


def get_data_with_pagination(
    db: Session,
    tableName: DeclarativeMeta,
    page: int,
    size: int,
    filter_by: ColumnElement[bool] | None = None,
) -> List[models.Order] | None:

    query = db.query(tableName)

    if filter_by is not None:
        query = query.filter(filter_by)

    return query.offset(page - 1).limit(size).all()
