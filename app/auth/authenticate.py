from app.auth import hashing
from app.crud import get_user

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not hashing.verify_password(password, user.hashed_password):
        return False
    return user
