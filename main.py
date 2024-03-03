from fastapi import FastAPI
from .import schemas
app = FastAPI()

@app.post('/admin/init')
async def add_admin(admin:schemas.Admin):
    return admin

@app.post('/user/init')
async def add_user(user:schemas.User):
    return user

@app.get('/gameslist/')
async def show_games_list():
    pass

@app.post('/orderagame/{game_id}')
async def order_a_game(game_id:int,order:schemas.Order):
    pass




