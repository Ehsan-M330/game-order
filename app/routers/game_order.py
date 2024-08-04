from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import SessionLocal
from typing import Annotated


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    


    
@router.post('/user/signup')
async def add_user(user:schemas.UserIn,db:Session=Depends(get_db)):
    crud.create_user(db=db,user=user)
    return {}

@router.post('/admin/singup')
async def add_admin(admin:schemas.AdminIn,db: Session=Depends(get_db)):
    crud.create_admin(db=db,admin=admin)
    return {}



@router.get('/gameslist/')
async def show_games_list(db:Session=Depends(get_db)):
    return crud.get_games(db=db)

@router.post('/orderagame/{game_id}')
async def order_a_game(game_id:int,order:schemas.Order):
    pass






