from  app.database.db import Base
from datetime import date, time
from sqlalchemy import Date, Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column

class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(12), nullable=False)

    booking_date: Mapped[date] = mapped_column(Date, nullable=False)
    booking_time: Mapped[time] = mapped_column(Time, nullable=False)

    guests: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(10), default="active", nullable=False)
