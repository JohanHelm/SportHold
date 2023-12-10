from app.domain.models.rental.dto import RentalCreate, RentalGet
from app.infra.db.models.rental.schema import Rental
from sqlalchemy.future import select


class RentalDAO:
    async def create(self, _session, _rental: RentalCreate):
        sa_rental_add: Rental = Rental(**_rental.model_dump())
        async with _session() as session:
            session.add(sa_rental_add)
            await session.commit()
        get_rental_pydantic = RentalGet.model_validate(sa_rental_add)
        return get_rental_pydantic

    async def show_rentals(self, _session):
        async with _session() as session:
            result = await session.execute(select(Rental))
            rentals = result.scalars().all()
        return rentals
