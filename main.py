from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.post('/user/signup')
async def add_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    crud.create_user(db=db,user=user)
    return {}

@app.post('/admin/signin')
async def add_admin(admin:schemas.Admin,db: Session=Depends(get_db)):
    db_item=models.Admin(**admin.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item



@app.get('/gameslist/')
async def show_games_list():
    pass

@app.post('/orderagame/{game_id}')
async def order_a_game(game_id:int,order:schemas.Order):
    pass




