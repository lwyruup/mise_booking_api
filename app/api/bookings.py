from fastapi import APIRouter, HTTPException, Depends, status, Query
from datetime import date
from typing import Annotated

from app.database.db import get_db_session, AsyncSession
from app.schemas.booking import BookingCreate, BookingOut
from app.services.bookings_service import (
    cancel_booking,
    create_booking,
    get_booking_by_id,
    get_bookings,
    booking_slot_is_taken,)

router = APIRouter(prefix="/bookings", tags=["bookings"])

SessionDep = Annotated[AsyncSession, Depends(get_db_session)]

@router.post("", response_model=BookingOut, status_code=status.HTTP_201_CREATED)
async def create_booking_endpoint(booking_data: BookingCreate, session: SessionDep) -> BookingOut:
    if await booking_slot_is_taken(session, booking_data):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Данный слот уже занят",
        )

    return await create_booking(session, booking_data)

@router.get("", response_model=list[BookingOut])
async def get_bookings_endpoint(
        session: SessionDep,
        date: date | None = None,
        limit: int = Query(default=20, ge=1, le=100),
        offset: int = Query(default=0, ge=0),
) -> list[BookingOut]:
    return await get_bookings(session, date, limit, offset)


@router.get("/{booking_id}", response_model=BookingOut)
async def get_booking_endpoint(booking_id: int, session: SessionDep) -> BookingOut:
    booking = await get_booking_by_id(session, booking_id)

    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )
    return booking

@router.delete("/{booking_id}", response_model=BookingOut)
async def cancel_booking_endpoint(booking_id: int, session: SessionDep) -> BookingOut:
    booking = await get_booking_by_id(session, booking_id)

    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )
    return await cancel_booking(session, booking)