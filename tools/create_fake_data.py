# app/seed_data.py

import sys
import os

# Add the project's root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User, Profile, Game, Order
from app.auth.hashing import get_password_hash
from tools.fake_data import (
    generate_fake_username,
    generate_fake_name,
    generate_fake_last_name,
    generate_fake_phone_number,
    generate_fake_price,
    generate_fake_id,  # type: ignore
    generate_fake_game_name,
    generate_fake_date,
    generate_fake_steam_id,
    generate_fake_role,  # type: ignore
    generate_fake_password,
    generate_fake_order_status,
)
from enums.user_roles import UserRole
import random


def create_fake_user(session: Session):
    while True:
        username = generate_fake_username()
        existing_username = (
            session.query(User).filter(User.username == username).first()
        )
        if not existing_username:
            break

    fake_user = User(
        username=username,
        hashed_password=get_password_hash("password"),
        name=generate_fake_name(),
        last_name=generate_fake_last_name(),
        phone_number=generate_fake_phone_number(),
        role=UserRole.USER,
    )
    create_fake_profile(session=session, user=fake_user)
    session.add(fake_user)
    session.commit()
    return fake_user


def create_fake_admin(session: Session):
    while True:
        username = generate_fake_username()
        existing_username = (
            session.query(User).filter(User.username == username).first()
        )
        if not existing_username:
            break

    fake_admin = User(
        username=username,
        hashed_password=get_password_hash("password"),
        name=generate_fake_name(),
        last_name=generate_fake_last_name(),
        phone_number=generate_fake_phone_number(),
        role=UserRole.ADMIN,
    )
    session.add(fake_admin)
    session.commit()
    return fake_admin


def create_fake_profile(session: Session, user: User):
    fake_profile = Profile(
        user_id=user.id,
        steam_username=generate_fake_username(),
        steam_password=generate_fake_password(),
    )
    session.add(fake_profile)
    session.commit()
    return fake_profile


def create_fake_game(session: Session):
    while True:
        steam_id = generate_fake_steam_id()
        existing_game = session.query(Game).filter(Game.steam_id == steam_id).first()
        if not existing_game:
            break

    fake_game = Game(
        name=generate_fake_game_name(),
        author=generate_fake_name(),
        steam_id=steam_id,
        price=generate_fake_price(),
    )
    session.add(fake_game)
    session.commit()
    return fake_game


def create_fake_order(session: Session, user: User, game: Game):
    fake_order = Order(
        user_id=user.id,
        game_id=game.id,
        status=generate_fake_order_status(),
        order_date=generate_fake_date(),
    )
    session.add(fake_order)
    session.commit()
    return fake_order


def populate_database(
    session: Session,
    num_admins: int = 5,
    num_users: int = 10,
    num_games: int = 10,
    num_orders: int = 20,
):
    # Create fake users and profiles
    for _ in range(num_users):
        user = create_fake_user(session)

    # Create fake admins
    for _ in range(num_admins):
        create_fake_admin(session)

    # Create fake games
    for _ in range(num_games):
        create_fake_game(session)

    # Create fake orders
    users = session.query(User).all()
    games = session.query(Game).all()

    if not users or not games:
        raise ValueError("No users or games available to create an order.")

    for _ in range(num_orders):
        user = random.choice(users)
        game = random.choice(games)
        create_fake_order(session, user, game)


if __name__ == "__main__":

    # Create a new database session
    session = SessionLocal()

    # Populate the database with fake data
    populate_database(session)

    # Close the session
    session.close()
    print("Done")
