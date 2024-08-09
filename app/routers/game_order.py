from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from app import crud, models, schemas
from app.database import SessionLocal
from typing import Annotated
import math

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
def calculate_total_data(db,tableName):
    #return db.execute(text(f"SELECT reltuples AS estimated_count FROM pg_class WHERE relname = '{tableName}';")).scalar()
    return db.query(tableName).count()

@router.post('/user/signup',status_code=status.HTTP_201_CREATED)
async def add_user(user:schemas.UserIn,db:Session=Depends(get_db)):
    crud.create_user(db=db,user=user)
    return {"message": "User created successfully"}

@router.post('/admin/singup',status_code=status.HTTP_201_CREATED)
async def add_admin(admin:schemas.AdminIn,db: Session=Depends(get_db)):
    crud.create_admin(db=db,admin=admin)
    return {"message": "Admin created successfully"}

@router.get('/gameslist/')
async def show_games_list(size:int=10,page:int=1,db:Session=Depends(get_db)):
    total_data=calculate_total_data(db=db,tableName=models.Game)
    total_pages=math.ceil(total_data / size)
    data = crud.get_games(db=db,page=page,size=size)
    return {
        "data": data,
        "total_data": total_data,
        "total_pages": total_pages,}

@router.get('/orderslist/')
async def show_orders_list(db:Session=Depends(get_db)):
    return crud.get_games(db=db)

@router.post('/orderagame/{game_id}')
async def order_a_game(game_id:int,order:schemas.Order):
    pass






