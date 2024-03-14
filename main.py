from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import uvicorn

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
async def add_user(user:schemas.UserIn,db:Session=Depends(get_db)):
    crud.create_user(db=db,user=user)
    return {}

@app.post('/admin/singup')
async def add_admin(admin:schemas.AdminIn,db: Session=Depends(get_db)):
    crud.create_admin(db=db,admin=admin)
    return {}



@app.get('/gameslist/')
async def show_games_list():
    pass

@app.post('/orderagame/{game_id}')
async def order_a_game(game_id:int,order:schemas.Order):
    pass

if __name__=="__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)





