from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.abstract import InfoForInvestAbstractModel

REPRESENTATION_TEXT = 'Пожертвование {id}, от {user_id}'


class Donation(InfoForInvestAbstractModel):
    """Модель пожертвования."""

    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self):
        return (
            REPRESENTATION_TEXT.format(id=self.id, user_id=self.user_id) +
            super().__repr__()
        )
