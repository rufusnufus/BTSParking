from sqlalchemy import Column, Integer, String, Float, Table, and_
import time
from app.db import db, metadata

cars = Table(
    "cars",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String),
    Column("model", String, nullable=False),
    Column("license_number", String, nullable=False),
)

users = Table(
    "users",
    metadata,
    Column("email", String, primary_key=True),
    Column("token", String),
    Column("token_expire_time", Float),
    Column("cookie", String)
)

class User: 
    @classmethod
    async def create(cls, **user):
        query = users.insert().values(**user)
        user_id = await db.execute(query)
        return user_id
    
    @classmethod
    async def get(cls, email):
        query = users.select().where(users.c.email == email)
        user = await db.fetch_one(query)
        return user

    @classmethod
    async def delete(cls, email):
        query = users.delete().where(users.c.email == email)
        await db.execute(query)
        return email

    @classmethod
    async def set_magic_link(cls, email, token, token_expire_time):
        query = users.update().where(users.c.email == email).values(
            token=token,  
            token_expire_time=token_expire_time
        )
        user = await db.execute(query)
        return user

    @classmethod
    async def validate_magic_link(cls, token):
        query = users.select().where(users.c.token == token)
        user = await db.fetch_one(query)
        
        if time.time() < dict(user)['token_expire_time']: 
            return dict(user)['email']
        
        return None

    @classmethod
    async def delete_magic_link(cls, email):
        query = users.update().where(users.c.email == email).values(
            token=None, 
            token_expire_time=None
        )
        user = await db.execute(query)
        return user 

    @classmethod
    async def set_cookie(cls, email, cookie):
        query = users.update().where(users.c.email == email).values(
            cookie=cookie,  
        )
        user = await db.execute(query)
        return user
    
    @classmethod
    async def check_cookie(cls, cookie):
        query = users.select().where(users.c.cookie == cookie)
        email = await db.execute(query)
        return email



class Car:
    @classmethod
    async def get(cls, id, email):
        query = cars.select().where(and_(cars.c.id == id, cars.c.email == email))
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
        return car_id
    
    @classmethod
    async def delete(cls, id, email):
        query = cars.delete().where(and_(cars.c.id == id, cars.c.email == email))
        car_id = await db.execute(query)
        return car_id
