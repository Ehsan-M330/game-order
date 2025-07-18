from datetime import timedelta
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.auth import authenticate, dependencies, tokens
from app.database import SessionLocal
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from sqlalchemy.exc import SQLAlchemyError
from typing import Annotated
import jwt
from app.auth.dependencies import SECRET_KEY, ALGORITHM
from enums.user_roles import UserRole
from app.utils.pagination_helpers import (
    calculate_total_data,
    validate_pagination_parameters,
)
import math

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception

    except InvalidTokenError:
        raise credentials_exception
    user = crud.get_user_byUsername(db, username=username)
    if user is None:
        raise credentials_exception
    return user


user_dependency = Annotated[schemas.TokenData, Depends(get_current_user)]


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> schemas.Token:

    user = authenticate.authenticate_user(db, form_data.username, form_data.password)
    if user == None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=dependencies.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = tokens.create_access_token(
        data=schemas.TokenData(id=user.id, username=user.username, role=user.role),
        expires_delta=access_token_expires,
    )
    return schemas.Token(access_token=access_token, token_type="bearer")


@router.post("/addgame/", status_code=status.HTTP_201_CREATED)
async def add_game(
    user: user_dependency, game: schemas.GameIn, db: Session = Depends(get_db)
):
    if user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this resource",
        )
    crud.create_game(db=db, game=game)
    return {"message: Game added successfully"}


@router.post("/orderagame/", status_code=status.HTTP_201_CREATED)
async def order_a_game(
    user: user_dependency, order: schemas.OrderIn, db: Session = Depends(get_db)
):
    if user.role == UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Users can order a game",
        )
    if crud.check_order(db=db, order=order) == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong input"
        )

    crud.create_order(db=db, order=order, user_id=user.id)
    return {"message: Order added successfully"}


@router.get("/myorders", response_model=schemas.OrdersListResponse)
async def get_user_orders(
    user: user_dependency, size: int = 10, page: int = 1, db: Session = Depends(get_db)
) -> schemas.OrdersListResponse:
    if user.role == UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Users can see their orders",
        )
    try:
        # Validate the input parameters
        validate_pagination_parameters(size=size, page=page)

        # Calculate the total number of data entries
        total_data = calculate_total_data(
            db=db, tableName=models.Order, filter_by=models.Order.user_id == user.id
        )

        # Calculate total pages and validate the page number
        total_pages = math.ceil(total_data / size)

        if total_pages == 0:
            return schemas.OrdersListResponse(
                data=[], total_data=0, total_pages=0, message="No orders found."
            )

        if page > total_pages:
            raise HTTPException(
                status_code=404, detail="Page number exceeds total pages."
            )

        # Fetch the data
        data = crud.get_data_with_pagination(
            db=db,
            tableName=models.Order,
            page=page,
            size=size,
            filter_by=models.Order.user_id == user.id,
        )

        # Handle empty data sets
        if not data:
            return schemas.OrdersListResponse(
                data=[],
                total_data=total_data,
                total_pages=total_pages,
                message="No games found.",
            )
        data = [data.__dict__ for data in data]

        return schemas.OrdersListResponse(
            data=[schemas.OrderOut.model_validate(data) for data in data],
            total_data=total_data,
            total_pages=total_pages,
        )

    except SQLAlchemyError:
        # Handle database errors
        raise HTTPException(
            status_code=500, detail="An error occurred while accessing the database."
        )
