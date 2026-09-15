from fastapi import FastAPI
from app.api.bookings import router as bookings_router

app = FastAPI(
    title="MISE Booking API"
)

app.include_router(bookings_router)