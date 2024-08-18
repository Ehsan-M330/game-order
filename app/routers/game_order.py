from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app import crud, models, schemas
from app.database import SessionLocal
from typing import Type, List, Union
import math

router = APIRouter()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def calculate_total_data(table: Type[models.Base], db: Session) -> int:
    return db.query(table).count()


async def fetch_paginated_data(
    model: Type[models.Base],
    schema_out: Type[schemas.BaseModel],
    crud_func: callable,
    size: int,
    page: int,
    db: Session,
) -> Union[schemas.BaseModel, HTTPException]:
    # Validate the input parameters
    if size <= 0 or page <= 0:
        raise HTTPException(
            status_code=400, detail="Size and page must be greater than zero."
        )

    # Calculate total data and pages
    total_data = calculate_total_data(table=model, db=db)
    total_pages = math.ceil(total_data / size)

    if total_pages == 0:
        return schema_out(
            data=[], total_data=0, total_pages=0, message="No data found."
        )
    if page > total_pages:
        raise HTTPException(status_code=404, detail="Page number exceeds total pages.")

    # Fetch the data
    data = crud_func(db=db, page=page, size=size)

    # Handle empty data sets
    if not data:
        return schema_out(
            data=[],
            total_data=total_data,
            total_pages=total_pages,
            message="No data found.",
        )

    # Validate and convert ORM objects to schema models
    return schema_out(
        data=[schema_out.model_validate(item) for item in data],
        total_data=total_data,
        total_pages=total_pages,
    )


@router.post("/user/signup", status_code=status.HTTP_201_CREATED)
async def add_user(user: schemas.UserIn, db: Session = Depends(get_db)):
    crud.create_user(db=db, user=user)
    return {"message": "User created successfully"}


@router.post("/admin/signup", status_code=status.HTTP_201_CREATED)
async def add_admin(admin: schemas.AdminIn, db: Session = Depends(get_db)):
    crud.create_admin(db=db, admin=admin)
    return {"message": "Admin created successfully"}


@router.get("/gameslist/", response_model=schemas.GamesListResponse)
async def show_games_list(
    size: int = 10, page: int = 1, db: Session = Depends(get_db)
) -> schemas.GamesListResponse:
    try:
        return await fetch_paginated_data(
            model=models.Game,
            schema_out=schemas.GameOut,
            crud_func=crud.get_games,
            size=size,
            page=page,
            db=db,
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500, detail="An error occurred while accessing the database."
        )


@router.get("/orderslist/", response_model=schemas.OrdersListResponse)
async def show_orders_list(
    size: int = 10, page: int = 1, db: Session = Depends(get_db)
) -> schemas.OrdersListResponse:
    try:
        return await fetch_paginated_data(
            model=models.Order,
            schema_out=schemas.OrderOut,
            crud_func=crud.get_orders,
            size=size,
            page=page,
            db=db,
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500, detail="An error occurred while accessing the database."
        )
