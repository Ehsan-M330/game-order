from datetime import datetime, timedelta, timezone
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.auth import authenticate,dependencies,tokens
from app.database import SessionLocal, engine
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from typing import Annotated


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db:Session=Depends(get_db)
) -> schemas.Token:
    user = authenticate.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=dependencies.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = tokens.create_access_token(
        data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")
    
@router.post('/user/signup')
async def add_user(user:schemas.UserIn,db:Session=Depends(get_db)):
    crud.create_user(db=db,user=user)
    return {}

@router.post('/admin/singup')
async def add_admin(admin:schemas.AdminIn,db: Session=Depends(get_db)):
    crud.create_admin(db=db,admin=admin)
    return {}


@router.post('/addgame/')
async def add_game(game:schemas.GameIn,db:Session=Depends(get_db)):
    crud.create_game(db=db,game=game)
    return {}
@router.get('/gameslist/')
async def show_games_list(db:Session=Depends(get_db)):
    return crud.get_games(db=db)

@router.post('/orderagame/{game_id}')
async def order_a_game(game_id:int,order:schemas.Order):
    pass






