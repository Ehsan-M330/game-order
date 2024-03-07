from fastapi import FastAPI,Depends
from files import schemas,models
from sqlalchemy.orm import Session
from files.database import SessionLocal,engine
app = FastAPI()

models.Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def signIn_admin(db: Session=Depends(get_db),admin=schemas.Admin):
    db_item=models.Admin(**schemas.Admin)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
@app.post('/admin/signin')
async def add_admin(admin:schemas.Admin,db: Session=Depends(get_db)):
    db_item=models.Admin(**admin.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.post('/user/signin')
async def add_user(user:schemas.User):
    return user

@app.get('/gameslist/')
async def show_games_list():
    pass

@app.post('/orderagame/{game_id}')
async def order_a_game(game_id:int,order:schemas.Order):
    pass




