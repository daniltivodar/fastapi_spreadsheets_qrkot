from http import HTTPStatus

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import SPREADSHEETS_URL
from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.services.google_api import (
    set_user_permissions, spreadsheets_create, spreadsheets_update_value,
)

router = APIRouter()


@router.get(
    '/',
    response_model=list[dict[str, str]],
    dependencies=(Depends(current_superuser),),
)
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_service: Aiogoogle = Depends(get_service),
) -> list[dict[str, str]]:
    """Получение таблицы GoogleSheets. Только для суперюзеров."""
    charity_projects = (
        await charity_project_crud.get_projects_by_completion_rate(session)
    )
    spreadsheet_id = await spreadsheets_create(wrapper_service)
    await set_user_permissions(spreadsheet_id, wrapper_service)
    try:
        await spreadsheets_update_value(
            spreadsheet_id, charity_projects, wrapper_service,
        )
    except ValueError as error:
        raise HTTPException(HTTPStatus.BAD_REQUEST, error)
    return SPREADSHEETS_URL.format(spreadsheet_id=spreadsheet_id)
