from datetime import timedelta
from typing import Optional

from sqlalchemy import extract, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject

CLOSE_TIME_FORMAT = '{days} days, {time}'


class CRUDCharityProject(CRUDBase):
    """Расширенный класс методов CRUD для благотворительных проектов."""

    async def get_charity_project_id_by_name(
        self, charity_project_name: str, session: AsyncSession,
    ) -> Optional[int]:
        """Возвращает id объекта модели с искомым именем."""
        return (
            await session.execute(
                select(self.model).where(
                    self.model.name == charity_project_name,
                ),
            )
        ).scalars().first()

    async def get_projects_by_completion_rate(
        self, session: AsyncSession,
    ) -> list[dict[str, str]]:
        """
        Возвращает закрытые проекты отсортированные по скорости закрытия.
        """
        charity_projects = (
            await session.execute(
                select(
                    self.model.name,
                    (
                        extract('epoch', self.model.close_date) -
                        extract('epoch', self.model.create_date)
                    ).label('close_time'),
                    self.model.description,
                ).where(
                    self.model.fully_invested == 1,
                ).order_by('close_time'),
            )
        ).all()
        return [
            {
                'charity_project_name': charity_project_name,
                'close_time': CLOSE_TIME_FORMAT.format(
                    days=timedelta(seconds=close_time).days,
                    time=timedelta(seconds=close_time),
                ),
                'description': charity_project_description,
            }
            for charity_project_name, close_time, charity_project_description
            in charity_projects
        ]


charity_project_crud = CRUDCharityProject(CharityProject)
