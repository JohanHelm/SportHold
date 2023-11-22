from pydantic import BaseModel, ConfigDict


class RentalBase(BaseModel):
    category: str = None
    name: str = None
    description: str = None

    model_config = ConfigDict(from_attributes=True)


class RentalCreate(RentalBase):
    ...


class RentalGet(RentalBase):
    id: int
