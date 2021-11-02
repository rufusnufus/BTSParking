from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Table

from app.db import db, metadata, sqlalchemy

cars = Table(
    "cars",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("model", String),
    Column("license_number", String),
)

class Car:
    @classmethod
    async def get(cls, id):
        query = cars.select().where(cars.c.id == id)
        car = await db.fetch_one(query)
        return car
    
    @classmethod
    async def get_all(cls):
        query = cars.select()
        user_cars = await db.fetch_all(query)
        return user_cars

    @classmethod
    async def create(cls, **car):
        query = cars.insert().values(**car)
        car_id = await db.execute(query)
        return car_id
    
    @classmethod
    async def delete(cls, id):
        query = cars.delete().where(cars.c.id == id)
        await db.execute(query)
        return id
