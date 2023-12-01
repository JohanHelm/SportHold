from pydantic import BaseModel, ConfigDict


class TarifBase(BaseModel):

    rentals_amount: int  # В этом столбце количество предоставляемых расписаний (объектов)
    one_month: int  # стоимость при оплате за период
    three_month: int
    six_month: int
    one_year: int
    two_years: int
    three_years: int

    model_config = ConfigDict(from_attributes=True)


class TarifCreate(TarifBase):
    ...


class TarifGet(TarifBase):
    ...
