from datetime import date, timedelta

import pytest
from httpx import AsyncClient


def booking_payload(**overrides):
    payload = {
        "name": "Иван Петров",
        "phone": "+79182225555",
        "booking_date": (date.today() + timedelta(days=1)).isoformat(),
        "booking_time": "18:00:00",
        "guests": 3,
    }
    payload.update(overrides)
    return payload


@pytest.mark.asyncio
async def test_create_booking(client: AsyncClient):
    response = await client.post(
        "/bookings",
        json=booking_payload(),
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Иван Петров"
    assert data["phone"] == "+79182225555"
    assert data["guests"] == 3
    assert data["status"] == "active"
    assert "id" in data


@pytest.mark.asyncio
async def test_get_booking_by_id(client: AsyncClient):
    create_response = await client.post(
        "/bookings",
        json=booking_payload(),
    )
    booking_id = create_response.json()["id"]

    response = await client.get(f"/bookings/{booking_id}")

    assert response.status_code == 200
    assert response.json()["id"] == booking_id


@pytest.mark.asyncio
async def test_booking_not_found(client: AsyncClient):
    response = await client.get("/bookings/999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Booking not found"
    }


@pytest.mark.asyncio
async def test_get_bookings(client: AsyncClient):
    await client.post(
        "/bookings",
        json=booking_payload(),
    )

    response = await client.get("/bookings")

    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_filter_bookings_by_date(client: AsyncClient):
    first_date = (date.today() + timedelta(days=1)).isoformat()
    second_date = (date.today() + timedelta(days=2)).isoformat()

    await client.post(
        "/bookings",
        json=booking_payload(
            booking_date=first_date,
            booking_time="18:00:00",
        ),
    )

    await client.post(
        "/bookings",
        json=booking_payload(
            booking_date=second_date,
            booking_time="19:00:00",
        ),
    )

    response = await client.get(
        "/bookings",
        params={"date": first_date},
    )

    assert response.status_code == 200

    bookings = response.json()

    assert len(bookings) == 1
    assert bookings[0]["booking_date"] == first_date


@pytest.mark.asyncio
async def test_cancel_booking(client: AsyncClient):
    create_response = await client.post(
        "/bookings",
        json=booking_payload(),
    )
    booking_id = create_response.json()["id"]

    response = await client.delete(
        f"/bookings/{booking_id}"
    )

    assert response.status_code == 200
    assert response.json()["status"] == "cancelled"


@pytest.mark.asyncio
async def test_cancel_booking_not_found(client: AsyncClient):
    response = await client.delete("/bookings/999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Booking not found"
    }


@pytest.mark.asyncio
async def test_booking_conflict(client: AsyncClient):
    payload = booking_payload()

    first_response = await client.post(
        "/bookings",
        json=payload,
    )

    second_response = await client.post(
        "/bookings",
        json=payload,
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json() == {
        "detail": "Данный слот уже занят"
    }


@pytest.mark.asyncio
async def test_cancelled_slot_can_be_booked_again(
    client: AsyncClient,
):
    payload = booking_payload()

    create_response = await client.post(
        "/bookings",
        json=payload,
    )
    booking_id = create_response.json()["id"]

    await client.delete(f"/bookings/{booking_id}")

    response = await client.post(
        "/bookings",
        json=payload,
    )

    assert response.status_code == 201
    assert response.json()["status"] == "active"


@pytest.mark.asyncio
async def test_invalid_guests(client: AsyncClient):
    response = await client.post(
        "/bookings",
        json=booking_payload(guests=13),
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_invalid_booking_time(client: AsyncClient):
    response = await client.post(
        "/bookings",
        json=booking_payload(
            booking_time="18:30:00"
        ),
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_invalid_phone(client: AsyncClient):
    response = await client.post(
        "/bookings",
        json=booking_payload(
            phone="12345"
        ),
    )

    assert response.status_code == 422