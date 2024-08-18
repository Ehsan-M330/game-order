from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.sql.elements import ColumnElement
from typing import Type
from fastapi import HTTPException


def calculate_total_data(
    tableName: Type[DeclarativeMeta],
    db: Session,
    filter_by: ColumnElement[bool] | None = None,
) -> int:
    # return db.execute(text(f"SELECT reltuples AS estimated_count FROM pg_class WHERE relname = '{tableName}';")).scalar()
    query = db.query(tableName)

    if filter_by is not None:
        query = query.filter(filter_by)

    return query.count()


def validate_pagination_parameters(page: int, size: int):
    if size <= 0 or page <= 0:
        raise HTTPException(
            status_code=400, detail="Size and page must be greater than zero."
        )
