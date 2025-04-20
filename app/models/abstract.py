from datetime import datetime as dt

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.db import Base

REPRESENTATION_TEXT = (
    ' дата создания {create_date}, '
    'дата закрытия {close_date}, '
    'необходимое кол-во инвестиций {full_amount}, '
    'внесенная сумма инвестиций{invested_amount}'
)


class InfoForInvestAbstractModel(Base):
    """Базовый класс для благотворительных проектов и пожертвований."""
    __abstract__ = True

    full_amount = Column(Integer, default=0)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(
        DateTime, default=dt.now,
    )
    close_date = Column(DateTime)

    __table_args__ = (
        CheckConstraint('full_amount > 0', 'full_amount greater then zero'),
        CheckConstraint(
            '0 <= invested_amount <= full_amount',
            'invested amount greater or equal 0, '
            'and lower or equal full_amount',
        ),
    )

    def __repr__(self):
        return (
            REPRESENTATION_TEXT.format(
                create_date=self.create_date,
                close_date=self.close_date,
                full_amount=self.full_amount,
                invested_amount=self.invested_amount,
            )
        )
