from datetime import datetime, timedelta, timezone
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.auth import authenticate,dependencies,tokens
from app.database import SessionLocal
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from typing import Annotated
import jwt
from app.auth.dependencies import SECRET_KEY, ALGORITHM
from enums.user_roles import UserRole

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db:Session=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        
    except InvalidTokenError:
        raise credentials_exception
    user = crud.get_user(db, username=username)
    if user is None:
        raise credentials_exception
    return user

user_dependency=Annotated[schemas.TokenData,Depends(get_current_user)]

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
        user, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")

@router.post('/addgame/',status_code=status.HTTP_201_CREATED)
async def add_game(user:user_dependency, game:schemas.GameIn,db:Session=Depends(get_db)):
    if user.role!=UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this resource",
        )   
    crud.create_game(db=db,game=game)
    return {"message: Game added successfully"}