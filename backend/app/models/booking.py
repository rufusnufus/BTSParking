from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String, Table,
                        select)

from app.db import db, metadata

bookings = Table(
    "bookings",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("booked_from", DateTime),
    Column("booked_until", DateTime),
    Column("space_id", Integer, ForeignKey("spaces.id")),
    Column("car_id", Integer, ForeignKey("cars.id"), index=True),
    Column("email", String, ForeignKey("users.email"), index=True),
)


class Booking:
    @classmethod
    async def get_bookings(cls, email):
        query = select(
            bookings.c.booked_from,
            bookings.c.booked_until,
            bookings.c.space_id,
            bookings.c.car_id,
        ).where(bookings.c.email == email)
        user_bookings = await db.fetch_all(query)
        return user_bookings

    @classmethod
    async def add_booking(cls, **booking):
        query = bookings.insert().values(**booking)
        user_booking = await db.execute(query)
        return user_booking
