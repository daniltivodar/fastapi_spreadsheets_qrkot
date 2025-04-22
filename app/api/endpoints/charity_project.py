from datetime import datetime as dt, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_availability_to_delete,
    check_availability_to_modify,
    check_charity_project_exist,
    check_full_amount_not_lower_than_invested_amount,
    check_name_duplicate,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate,
)
from app.services.investment import investment

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список всех проектов."""
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=(Depends(current_superuser),),
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.

    Создаёт благотворительный проект.
    """
    await check_name_duplicate(charity_project.name, session)
    project = await charity_project_crud.create(
        charity_project, session, commit=False,
    )
    session.add_all(
        investment(
            project,
            await donation_crud.get_not_fully_invested(session),
        ),
    )
    await session.commit()
    await session.refresh(project)
    return project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=(Depends(current_superuser),),
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.

    Закрытый проект нельзя редактировать; нельзя
    установить требуемую сумму меньше уже вложенной.
    """
    charity_project = await check_charity_project_exist(
        project_id, session,
    )
    check_availability_to_modify(charity_project.close_date)
    if obj_in.full_amount:
        check_full_amount_not_lower_than_invested_amount(
            obj_in.full_amount, charity_project.invested_amount,
        )
        if obj_in.full_amount == charity_project.invested_amount:
            charity_project.fully_invested = True
            charity_project.close_date = dt.now(timezone.utc)
    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)
    return (
        await charity_project_crud.update(
            charity_project, obj_in, session, commit=False,
        )
    )


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=(Depends(current_superuser),),
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.

    Удаляет проект. Нельзя удалить проект, в который уже
    были инвестированы средства, его можно только закрыть.
    """
    charity_project = await check_charity_project_exist(
        project_id, session,
    )
    check_availability_to_delete(
        charity_project.invested_amount, charity_project.close_date,
    )
    return await charity_project_crud.delete(charity_project, session)
