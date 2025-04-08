from datetime import datetime as dt
from typing import Optional

from pydantic import BaseModel, Extra, Field, validator

from services.constants import Limits


class CharityBase(BaseModel):
    name: Optional[str] = Field(
        min_length=Limits.CHARITY_BASE_NAME_MIN_LEN.value, 
        max_length=Limits.CHARITY_BASE_NAME_MAX_LEN.value
        )
    description: Optional[str] = Field(
        min_length=Limits.CHARITY_BASE_DES_MIN_LEN.value
        )
    full_amount: Optional[int] = Field(gt=0)

    class Config:
        extra = Extra.forbid


class CharityCreate(CharityBase):
    name: str = Field(
        ..., 
        min_length=Limits.CHARITY_CREATE_DES_MIN_LEN.value, 
        max_length=Limits.CHARITY_CREATE_NAME_MAX_LEN.value
        )
    description: str = Field(
        min_length=Limits.CHARITY_CREATE_DES_MIN_LEN.value
        )
    full_amount: int = Field(gt=0)


class CharityUpdate(CharityBase):
    pass

    @validator("name")
    def validate_name_is_not_none(cls, value):
        if value is None:
            # При ошибке валидации можно выбросить
            # ValueError, TypeError или AssertionError.
            # В нашем случае подходит ValueError.
            # В аргумент передаём сообщение об ошибке.
            raise ValueError("Имя переговорки не может быть пустым!")
        # Если проверка пройдена, возвращаем значение поля.
        return value


class CharityRepresintation(CharityBase):
    id: int
    invested_amount: int = Field(0)
    fully_invested: bool = Field(False)
    create_date: dt = Field(default_factory=dt.now)
    close_date: Optional[dt] = Field(None)

    class Config:
        orm_mode = True
