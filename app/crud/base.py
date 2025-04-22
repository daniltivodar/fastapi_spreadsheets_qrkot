from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class CRUDBase:
    """Базовый класс методов CRUD."""

    def __init__(self, model):
        self.model = model

    async def get(self, obj_id: int, session: AsyncSession):
        """Метод возвращает объект модели для чтения."""
        return (
            await session.execute(
                select(self.model).where(self.model.id == obj_id),
            )
        ).scalars().first()

    async def get_multi(self, session: AsyncSession):
        """Метод возвращает все объекты модели для чтения."""
        return (await session.execute(select(self.model))).scalars().all()

    async def get_not_fully_invested(self, session: AsyncSession):
        """
        Метод возвращает список объектов со значением fully_invested=False.
        """
        return (
            await session.execute(
                select(self.model).where(self.model.fully_invested == 0),
            )
        ).scalars().all()

    async def create(
        self,
        obj_in,
        session: AsyncSession,
        user: Optional[User] = None,
        commit=True,
    ):
        """Метод создает и возвращает новый объект модели."""
        obj_in = obj_in.dict()
        obj_in['invested_amount'] = 0
        if user:
            obj_in['user_id'] = user.id
        db_obj = self.model(**obj_in)
        session.add(db_obj)
        if commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def update(
        self, db_obj, obj_in, session: AsyncSession, commit=True,
    ):
        """Метод обновляет и возвращает измененный объект модели."""
        update_data = obj_in.dict(exclude_unset=True)
        for field in jsonable_encoder(db_obj):
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        if commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def delete(self, db_obj, session: AsyncSession):
        """Метод удаляет и возвращает удаленный объект модели."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj
