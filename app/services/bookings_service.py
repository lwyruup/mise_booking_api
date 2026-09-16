from datetime import date
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.booking import Booking
from app.schemas.booking import BookingCreate


async def booking_slot_is_taken(session: AsyncSession,booking_data: BookingCreate) -> bool:
    query = select(Booking.id).where(
        Booking.booking_date == booking_data.booking_date,
        Booking.booking_time == booking_data.booking_time,
        Booking.status == "active",
    )

    result = await session.execute(query)
    return result.scalar_one_or_none() is not None


async def create_booking(session: AsyncSession, booking_data: BookingCreate) -> Booking:
    booking = Booking(**booking_data.model_dump())

    session.add(booking)
    await session.commit()
    await session.refresh(booking)

    return booking


async def get_bookings(session: AsyncSession, booking_date: date | None = None) -> list[Booking]:
    query = select(Booking)

    if booking_date is not None:
        query = query.where(Booking.booking_date == booking_date)

    result = await session.execute(query)
    return list(result.scalars().all())


async def get_booking_by_id(session: AsyncSession, booking_id: int) -> Booking | None:
    return await session.get(Booking, booking_id)


async def cancel_booking(session: AsyncSession, booking: Booking) -> Booking:
    booking.status = "cancelled"
    await session.commit()
    await session.refresh(booking)

    return booking