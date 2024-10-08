from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text  # type: ignore
from app import crud, models, schemas
from app.database import SessionLocal
from typing import Annotated, Type  # type: ignore
from app.utils.pagination_helpers import (
    calculate_total_data,
    validate_pagination_parameters,
)
from app.utils.phone_number_verification import (
    create_random_verification_code,
    stor_code,
    check_code,
)
import math

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/user/signup",
    status_code=status.HTTP_200_OK,
    summary="Create a new user",
    description="Create a new user in the system",
)
async def add_user(user: schemas.UserIn, db: Session = Depends(get_db)):
    code = create_random_verification_code()
    await stor_code(key=f"verification_code:{user.phone_number}", value=code)
    print(code)
    return {
        "message": "Verification code sent to your phone number. Please verify to complete signup."
    }


@router.post(
    "/user/verify",
    status_code=status.HTTP_201_CREATED,
    summary="Verify phone number",
    description="Verify the phone number to complete the signup process",
)
async def verify_user(code: int, user: schemas.UserIn, db: Session = Depends(get_db)):
    # Step 1: Validate the verification code
    is_valid = await check_code(user.phone_number, code)

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification code",
        )

    # Step 2: Create the user in the database if the code is valid
    crud.create_user(db=db, user=user)
    return {"message": "Phone number verified and user created successfully"}


@router.post(
    "/admin/singup",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new admin",
    description="Create a new admin in the system",
)
async def add_admin(admin: schemas.AdminIn, db: Session = Depends(get_db)):
    crud.create_admin(db=db, admin=admin)
    return {"message": "Admin created successfully"}


@router.get("/gameslist/", response_model=schemas.GamesListResponse)
async def show_games_list(
    size: int = 10, page: int = 1, db: Session = Depends(get_db)
) -> schemas.GamesListResponse:
    try:
        # Validate the input parameters
        validate_pagination_parameters(size=size, page=page)

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
        data = crud.get_data_with_pagination(
            db=db, tableName=models.Game, page=page, size=size
        )

        # Handle empty data sets
        if not data:
            return schemas.GamesListResponse(
                data=[],
                total_data=total_data,
                total_pages=total_pages,
                message="No games found.",
            )
        data = [data.__dict__ for data in data]

        return schemas.GamesListResponse(
            data=[schemas.GameOut.model_validate(data) for data in data],
            total_data=total_data,
            total_pages=total_pages,
        )

    except SQLAlchemyError:
        # Handle database errors
        raise HTTPException(
            status_code=500, detail="An error occurred while accessing the database."
        )


@router.get("/orderslist/", response_model=schemas.OrdersListResponse)
async def show_orders_list(
    size: int = 10, page: int = 1, db: Session = Depends(get_db)
) -> schemas.OrdersListResponse:
    try:
        # Validate the input parameters
        validate_pagination_parameters(size=size, page=page)

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
        data = crud.get_data_with_pagination(
            db=db, tableName=models.Order, page=page, size=size
        )

        # Handle empty data sets
        if not data:
            return schemas.OrdersListResponse(
                data=[],
                total_data=total_data,
                total_pages=total_pages,
                message="No orders found.",
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
