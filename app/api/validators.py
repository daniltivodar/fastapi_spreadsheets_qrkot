from datetime import datetime as dt
from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import (
    CHARITY_PROJECT_NOT_FOUND,
    DUPLICATE_NAME_ERROR,
    FULL_AMOUNT_LOWER_THAN_INVESTED_AMOUNT_ERROR,
    PROJECT_CLOSED_ERROR,
    PROJECT_HAS_MONEY_ERROR,
)
from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject


async def check_charity_project_exist(
    charity_project_id: int, session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        charity_project_id, session,
    )
    if not charity_project:
        raise HTTPException(HTTPStatus.NOT_FOUND, CHARITY_PROJECT_NOT_FOUND)
    return charity_project


async def check_name_duplicate(
    charity_project_name: str, session: AsyncSession,
) -> None:
    if await charity_project_crud.get_charity_project_id_by_name(
        charity_project_name, session,
    ):
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            DUPLICATE_NAME_ERROR,
        )


def check_availability_to_delete(
    charity_project_invested_amount: int,
    charity_project_close_date: Optional[dt] = None,
) -> None:
    if charity_project_invested_amount != 0 or charity_project_close_date:
        raise HTTPException(HTTPStatus.BAD_REQUEST, PROJECT_HAS_MONEY_ERROR)


def check_availability_to_modify(
    charity_project_close_date: Optional[dt] = None,
) -> None:
    if charity_project_close_date:
        raise HTTPException(HTTPStatus.BAD_REQUEST, PROJECT_CLOSED_ERROR)


def check_full_amount_not_lower_than_invested_amount(
    full_amount: int, invested_amount: int,
) -> None:
    if full_amount < invested_amount:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            FULL_AMOUNT_LOWER_THAN_INVESTED_AMOUNT_ERROR,
        )
