from datetime import datetime as dt, timezone
from typing import Optional

from pydantic import BaseModel, Extra, Field, validator

from app.core.config import (
    EMPTY_NAME_ERROR,
    MAX_LEN_DESCRIPTION,
    MAX_LEN_NAME,
    MIN_LEN_STRING,
    MIN_VALUE_AMOUNT,
)


class CharityProjectBase(BaseModel):
    """Базовая схема благотворительного проекта."""

    name: Optional[str] = Field(
        None, min_length=MIN_LEN_STRING, max_length=MAX_LEN_NAME,
    )
    description: Optional[str] = Field(
        None, min_length=MIN_LEN_STRING, max_length=MAX_LEN_DESCRIPTION,
    )
    full_amount: Optional[int] = Field(None, gt=MIN_VALUE_AMOUNT)

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    """Схема для создания записи о благотворительном проекте."""

    name: str = Field(..., min_length=MIN_LEN_STRING, max_length=MAX_LEN_NAME)
    description: str = Field(
        ..., min_length=MIN_LEN_STRING, max_length=MAX_LEN_DESCRIPTION,
    )
    full_amount: int = Field(..., gt=MIN_VALUE_AMOUNT)


class CharityProjectUpdate(CharityProjectBase):
    """Схема для обновления записи о благотворительном проекте."""

    @validator('name')
    def name_cant_be_none(cls, value):
        if not value:
            raise ValueError(EMPTY_NAME_ERROR)
        return value


class CharityProjectDB(CharityProjectBase):
    """Схема вывода записи о благотворительном проекте в теле ответа."""

    id: int
    invested_amount: int
    fully_invested: bool
    create_date: dt = Field(
        ...,
        example=dt.now(
            timezone.utc,
        ).isoformat(timespec='minutes'),
    )
    close_date: Optional[dt] = Field(
        ...,
        example=dt.now(timezone.utc).isoformat(timespec='minutes'),
    )

    class Config:
        orm_mode = True
