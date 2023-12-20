import pytest

from app.domain.models.rental.dto import RentalBase, RentalType

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_renatal_model(rental_model: RentalBase):
    
    assert rental_model.rental_type == RentalType.REGULAR
    


