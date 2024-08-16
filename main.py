from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import auth, game_order

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(game_order.router)
app.include_router(auth.router)
