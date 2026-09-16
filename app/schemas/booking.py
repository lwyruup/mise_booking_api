import re
from datetime import date, time, timedelta
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class BookingBase(BaseModel):
    name: str = Field(min_length=2)
    phone: str
    booking_date: date
    booking_time: time
    guests: int = Field(ge=1, le=12)


class BookingCreate(BookingBase):
    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not re.fullmatch(r"[A-Za-zА-Яа-яЁё -]+", value):
            raise ValueError("Имя может содержать только буквы, пробелы и дефисы")
        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        if not re.fullmatch(r"(?:\+7|8)\d{10}", value):
            raise ValueError("Номер телефона должен быть в формате +7XXXXXXXXXX или 8XXXXXXXXXX")
        return value


    @field_validator("booking_date")
    @classmethod
    def validate_booking_date(cls, value: date) -> date:
        today = date.today()

        if value < today:
            raise ValueError("Дата бронирования не может быть в прошлом")

        if value > today + timedelta(days=90):
            raise ValueError("Дата бронирования не может быть более чем на 90 дней вперед")

        return value

    @field_validator("booking_time")
    @classmethod
    def validate_booking_time(cls, value: time) -> time:
        if value.minute != 0 or value.second != 0 or value.microsecond != 0:
            raise ValueError("Время бронирования должно содержать полный час")

        if not 12 <= value.hour <= 22:
            raise ValueError("Время бронирования должно быть с 12:00 до 22:00")

        return value


class BookingOut(BookingBase):
    id: int
    status: Literal["active", "cancelled"]

    model_config = ConfigDict(from_attributes=True)