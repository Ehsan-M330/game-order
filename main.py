from datetime import datetime, timedelta, timezone
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.auth import authenticate,dependencies,tokens
from app.database import SessionLocal, engine
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from typing import Annotated
from app.routers import auth, game_order

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(game_order.router)
app.include_router(auth.router)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()





