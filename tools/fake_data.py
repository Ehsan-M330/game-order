from faker import Faker
import random
from datetime import datetime
from enums.order_status import order_status

fake = Faker()


def generate_fake_username() -> str:
    return fake.user_name()


def generate_fake_name() -> str:
    return fake.first_name()


def generate_fake_last_name() -> str:
    return fake.last_name()


def generate_fake_phone_number() -> str:
    return fake.phone_number()


def generate_fake_price() -> float:
    return round(random.uniform(5, 60), 2)


def generate_fake_id() -> int:
    return fake.random_int(min=1, max=10000)


def generate_fake_date() -> datetime:
    return fake.date_time_this_year()


def generate_fake_steam_id() -> str:
    return str(fake.uuid4())


def generate_fake_game_name() -> str:
    return fake.word()


def generate_fake_role() -> str:
    return fake.word()


def generate_fake_password() -> str:
    return fake.password()


def generate_fake_order_status() -> order_status:
    return random.choice(list(order_status))
