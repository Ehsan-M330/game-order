from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text  # type: ignore
from app import crud, models, schemas
from app.database import SessionLocal
from typing import Annotated, Type  # type: ignore
import math

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def calculate_total_data(
    tableName: Type[models.Base], db: Session = Depends(get_db)  # type: ignore
) -> int:
    # return db.execute(text(f"SELECT reltuples AS estimated_count FROM pg_class WHERE relname = '{tableName}';")).scalar()
    return db.query(tableName).count()  # type: ignore


@router.post("/user/signup", status_code=status.HTTP_201_CREATED)
async def add_user(user: schemas.UserIn, db: Session = Depends(get_db)):
    crud.create_user(db=db, user=user)
    return {"message": "User created successfully"}


@router.post("/admin/singup", status_code=status.HTTP_201_CREATED)
async def add_admin(admin: schemas.AdminIn, db: Session = Depends(get_db)):
    crud.create_admin(db=db, admin=admin)
    return {"message": "Admin created successfully"}


@router.get("/gameslist/", response_model=schemas.GamesListResponse)
async def show_games_list(
    size: int = 10, page: int = 1, db: Session = Depends(get_db)
) -> schemas.GamesListResponse:
    try:
        # Validate the input parameters
        if size <= 0 or page <= 0:
            raise HTTPException(
                status_code=400, detail="Size and page must be greater than zero."
            )

        # Calculate the total number of data entries
        total_data = calculate_total_data(db=db, tableName=models.Game)

        # Calculate total pages and validate the page number
        total_pages = math.ceil(total_data / size)

        if total_pages == 0:
            return schemas.GamesListResponse(
                data=[], total_data=0, total_pages=0, message="No games found."
            )

        if page > total_pages:
            raise HTTPException(
                status_code=404, detail="Page number exceeds total pages."
            )

        # Fetch the data
        data = crud.get_games(db=db, page=page, size=size)

        # Handle empty data sets
        if not data:
            return schemas.GamesListResponse(
                data=[],
                total_data=total_data,
                total_pages=total_pages,
                message="No games found.",
            )

        return schemas.GamesListResponse(
            data=[],
            total_data=total_data,
            total_pages=total_pages,
            message="No games found.",
        )
    except SQLAlchemyError:
        # Handle database errors
        raise HTTPException(
            status_code=500, detail="An error occurred while accessing the database."
        )
    except Exception:
        # Catch any other exceptions
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


@router.get("/orderslist/", response_model=schemas.OrdersListResponse)
async def show_orders_list(
    size: int = 10, page: int = 1, db: Session = Depends(get_db)
) -> schemas.OrdersListResponse:
    try:
        # Validate the input parameters
        if size <= 0 or page <= 0:
            raise HTTPException(
                status_code=400, detail="Size and page must be greater than zero."
            )

        # Calculate the total number of data entries
        total_data = calculate_total_data(db=db, tableName=models.Order)

        # Calculate total pages and validate the page number
        total_pages = math.ceil(total_data / size)

        if total_pages == 0:
            return schemas.OrdersListResponse(
                data=[],
                total_data=0,
                total_pages=0,
                message="No orders found.",
            )
        if page > total_pages:
            raise HTTPException(
                status_code=404, detail="Page number exceeds total pages."
            )

        # Fetch the data
        data = crud.get_orders(db=db, page=page, size=size)

        # Handle empty data sets
        if not data:
            return schemas.OrdersListResponse(
                data=[],
                total_data=total_data,
                total_pages=total_pages,
                message="No orders found.",
            )
        return schemas.OrdersListResponse(
            data=[],
            total_data=total_data,
            total_pages=total_pages,
        )
    except SQLAlchemyError:
        # Handle database errors
        raise HTTPException(
            status_code=500, detail="An error occurred while accessing the database."
        )
    except Exception:
        # Catch any other exceptions
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
