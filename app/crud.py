from sqlalchemy.orm import Session
import hashlib
from app import models, schemas
from enums.user_roles import UserRole
from app.auth.hashing import get_password_hash

# def hash_password(password: str) -> str:
#     """Hashes a password using SHA-256."""
#     hashed_password = hashlib.sha256(password.encode()).hexdigest()
#     return hashed_password

def get_user(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()

def create_user(db: Session, user: schemas.UserIn):
    user.password = get_password_hash(user.password)
    
    db_user = models.User(
                                name=user.name,
                                last_name=user.last_name,
                                username=user.username,
                                hashed_password=user.password,
                                phone_number=user.phone_number,
                                role=UserRole.USER)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    db_profile = models.Profile(
                                steam_username=user.steam_username,
                                steam_password=user.steam_password,
                                user_id=db_user.id)
    
    db.add(db_profile)
    db.commit()

def create_admin(db: Session,admin:schemas.AdminIn):
    admin.password = get_password_hash(admin.password)
    db_admin = models.User( 
                            name=admin.name,
                            last_name=admin.last_name,
                            username=admin.username,
                            hashed_password=admin.password,
                            phone_number=admin.phone_number,
                            role=UserRole.ADMIN)
    db.add(db_admin)
    db.commit()
    
def create_game(db:Session,game:schemas.GameIn):
    db_game=models.Game(
                            name=game.name,
                            steam_id=game.steam_id,
                            author=game.author,
                            price=game.price)
    db.add(db_game)
    db.commit()
    
def get_games(db:Session,page,size):
    return db.query(models.Game).offset(page-1).limit(size).all()
    
    
def get_user(db:Session, username: str):
    user_dict=db.query(models.User).filter(models.User.username==username).first()
    return user_dict