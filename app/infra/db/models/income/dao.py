from app.domain.models.income.dto import IncomeCreate, IncomeGet
from app.infra.db.models.income.schema import Income


class IncomeDAO:
    async def create(self, _session, _income: IncomeCreate):
        sa_income_add: Income = Income(**_income.model_dump())
        async with _session() as session:
            session.add(sa_income_add)
            await session.commit()
        get_income_pydantic = IncomeGet.model_validate(sa_income_add)
        return get_income_pydantic
