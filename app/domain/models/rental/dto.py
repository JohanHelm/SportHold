from pydantic import BaseModel, ConfigDict


class RentalBase(BaseModel):
    category: str
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class RentalCreate(RentalBase):
    ...


class RentalGet(RentalBase):
    id: int
