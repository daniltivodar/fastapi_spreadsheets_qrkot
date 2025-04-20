from datetime import datetime as dt, timezone
from typing import Optional

from pydantic import BaseModel, Extra, Field

from app.core.config import MAX_LEN_DESCRIPTION, MIN_VALUE_AMOUNT


class DonationBase(BaseModel):
    """Базовая схема пожертвования."""

    full_amount: Optional[int] = Field(None, gt=MIN_VALUE_AMOUNT)
    comment: Optional[str] = Field(None, max_length=MAX_LEN_DESCRIPTION)

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    """Схема для создания записи о пожертвовании."""

    full_amount: int = Field(..., gt=MIN_VALUE_AMOUNT)


class DonationDBForUser(DonationBase):
    """Схема вывода записи для пользователя о пожертвовании в теле ответа."""

    id: int
    create_date: dt = Field(
        ...,
        example=dt.now(
            timezone.utc,
        ).isoformat(timespec='minutes'),
    )

    class Config:
        orm_mode = True


class DonationDBForAdmin(DonationDBForUser):
    """Схема вывода записи для админа о пожертвовании в теле ответа."""

    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[dt] = Field(
        ...,
        example=dt.now(timezone.utc).isoformat(timespec='minutes'),
    )
