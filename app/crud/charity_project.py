from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


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


charity_project_crud = CRUDCharityProject(CharityProject)
