from app.domain.models.order.dto import OrderCreate, OrderGet
from app.infra.db.models.order.schema import Order


class OrderDAO:
    async def create(self, _session, _order: OrderCreate):
        sa_order_add: Order = Order(**_order.model_dump())
        async with _session() as session:
            session.add(sa_order_add)
            await session.commit()
        get_order_pydantic = OrderGet.model_validate(sa_order_add)
        return get_order_pydantic
