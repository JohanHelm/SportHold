from app.domain.models.rental.dto import RentalCreate, RentalGet
from app.infra.db.models.rental.schema import Rental

# from app.domain.models.object.dto import ObjectCreate, ObjectGet
# from app.infra.db.models.object.schema import Object


# class ObjectDAO:
#     async def create(self, _session, _object: ObjectCreate):
#         sa_object_add: Object = Object(**_object.model_dump())
#         async with _session() as session:
#             session.add(sa_object_add)
#             await session.commit()
#         get_object_pydantic = ObjectGet.model_validate(sa_object_add)
#         return get_object_pydantic


class RentalDAO:
    async def create(self, _session, _rental: RentalCreate):
        sa_rental_add: Rental = Rental(**_rental.model_dump())
        async with _session() as session:
            session.add(sa_rental_add)
            await session.commit()
        get_rental_pydantic = RentalGet.model_validate(sa_rental_add)
        return get_rental_pydantic
