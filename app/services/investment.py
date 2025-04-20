from datetime import datetime as dt, timezone

from app.models.abstract import InfoForInvestAbstractModel


def investment(
    target: InfoForInvestAbstractModel,
    sources: list[InfoForInvestAbstractModel],
) -> list[InfoForInvestAbstractModel]:
    """Метод для инвестирования."""
    changed_sources = []

    for source in sources:
        min_sum = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount,
        )
        for item in [target, source]:
            item.invested_amount += min_sum
            if item.invested_amount == item.full_amount:
                item.fully_invested = True
                item.close_date = dt.now(timezone.utc)
        changed_sources.append(source)
        if target.fully_invested:
            break

    return changed_sources
