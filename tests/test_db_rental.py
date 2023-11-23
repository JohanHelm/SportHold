import pytest
from app.domain.models.rental.dto import RentalGet, RentalCreate
from app.infra.db.models.rental.dao import RentalDAO

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_rental_add(session, test_rental: RentalCreate):
    rental_dao = RentalDAO()
    created_rental: RentalGet = await rental_dao.create(session, test_rental)
    assert created_rental.name == test_rental.name
