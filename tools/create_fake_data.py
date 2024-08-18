import sys

# Add the project's root directory to sys.path
sys.path.append("d:/fastapi project/game-order")

from faker import Faker
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User, Profile, Game, Order
from app.auth.hashing import get_password_hash
from enums.user_roles import UserRole
from enums.order_status import order_status
import random

faker = Faker()


def create_fake_user(session: Session):
    while True:
        # Generate a unique username
        username = faker.user_name()

        # Check if this username already exists
        existing_username = (
            session.query(User).filter(User.username == username).first()
        )
        if not existing_username:
            break  # Unique username found, exit the loop

    fake_user = User(
        username=username,
        hashed_password=get_password_hash("password"),
        name=faker.first_name(),
        last_name=faker.last_name(),
        phone_number=faker.phone_number(),
        role=UserRole.USER,
    )
    create_fake_profile(session=session, user=fake_user)
    session.add(fake_user)
    session.commit()
    return fake_user


def create_fake_admin(session: Session):
    while True:
        # Generate a unique username
        username = faker.user_name()

        # Check if this username already exists
        existing_username = (
            session.query(User).filter(User.username == username).first()
        )
        if not existing_username:
            break  # Unique username found, exit the loop
    fake_admin = User(
        username=username,
        hashed_password=get_password_hash("password"),
        name=faker.first_name(),
        last_name=faker.last_name(),
        phone_number=faker.phone_number(),
        role=UserRole.ADMIN,
    )
    session.add(fake_admin)
    session.commit()
    return fake_admin


def create_fake_profile(session: Session, user: User):
    fake_profile = Profile(
        user_id=user.id,
        steam_username=faker.user_name(),
        steam_password=faker.password(),
    )
    session.add(fake_profile)
    session.commit()
    return fake_profile


def create_fake_game(session: Session):
    while True:
        # Generate a unique steam_id
        steam_id = faker.uuid4()

        # Check if this steam_id already exists
        existing_game = session.query(Game).filter(Game.steam_id == steam_id).first()
        if not existing_game:
            break  # Unique steam_id found, exit the loop

    fake_game = Game(
        name=faker.word(),
        author=faker.name(),
        steam_id=steam_id,
        price=round(random.uniform(5, 60), 2),
    )
    session.add(fake_game)
    session.commit()
    return fake_game


def create_fake_order(session: Session, user: User, game: Game):
    fake_order = Order(
        user_id=user.id,
        game_id=game.id,
        status=random.choice(list(order_status)),
        order_date=faker.date_time_this_year(),
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
