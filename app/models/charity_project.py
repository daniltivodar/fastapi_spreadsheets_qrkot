from sqlalchemy import Column, String, Text

from app.core.config import MAX_LEN_NAME
from app.models.abstract import InfoForInvestAbstractModel

REPRESENTATION_TEXT = 'Благотворительный проект {name}, {id}'


class CharityProject(InfoForInvestAbstractModel):
    """Модель благотворительного проекта."""

    name = Column(String(MAX_LEN_NAME), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (
            REPRESENTATION_TEXT.format(name=self.name, id=self.id) +
            super().__repr__()
        )
