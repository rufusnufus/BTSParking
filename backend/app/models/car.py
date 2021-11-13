from sqlalchemy import Column, ForeignKey, Integer, String, Table, and_

from app.db import db, metadata

cars = Table(
    "cars",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("email", String(64), ForeignKey("users.email"), index=True),
    Column("model", String, nullable=False),
    Column("license_number", String, nullable=False),
)


class Car:
    @classmethod
    async def get(cls, id, email=None):
        if email:
            query = cars.select().where(and_(cars.c.id == id, cars.c.email == email))
        else:
            query = cars.select().where(cars.c.id == id)
        car = await db.fetch_one(query)
        return car

    @classmethod
    async def get_all(cls, email):
        query = cars.select().where(cars.c.email == email)
        user_cars = await db.fetch_all(query)
        return user_cars

    @classmethod
    async def create(cls, **car):
        query = cars.insert().values(**car)
        car_id = await db.execute(query)
        query = cars.select().where(cars.c.id == car_id)
        created_car = await db.fetch_one(query)
        return created_car

    @classmethod
    async def delete(cls, id, email):
        query = cars.delete().where(and_(cars.c.id == id, cars.c.email == email))
        car_id = await db.execute(query)
        return car_id
