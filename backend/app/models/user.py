import time

from sqlalchemy import Boolean, Column, Float, String, Table, and_, select

from app.db import db, metadata

users = Table(
    "users",
    metadata,
    Column("email", String(64), primary_key=True, index=True),
    Column("token", String(64), index=True),
    Column("token_expire_time", Float),
    Column("cookie", String(256), index=True),
    Column("cookie_expire_time", Float),
    Column("is_admin", Boolean, default=False, nullable=False),
)


class User:
    @classmethod
    async def get_info(cls, email):
        query = select(users.c.email, users.c.is_admin).where(users.c.email == email)
        user = await db.fetch_one(query)
        return user

    @classmethod
    async def is_admin(cls, email):
        query = users.select(users.c.is_admin).where(
            and_(users.c.email == email, users.c.is_admin == True)
        )
        is_admin = await db.fetch_one(query)
        return is_admin

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
        query = (
            users.update()
            .where(users.c.email == email)
            .values(token=token, token_expire_time=token_expire_time)
        )
        user = await db.execute(query)
        return user

    @classmethod
    async def validate_magic_link(cls, token):
        query = users.select().where(users.c.token == token)
        user = await db.fetch_one(query)

        if user:
            if time.time() < dict(user)["token_expire_time"]:
                return dict(user)["email"]
        return None

    @classmethod
    async def delete_magic_link(cls, email):
        query = (
            users.update()
            .where(users.c.email == email)
            .values(token=None, token_expire_time=None)
        )
        user = await db.execute(query)
        return user

    @classmethod
    async def set_cookie(cls, email, cookie, cookie_expire_time):
        query = (
            users.update()
            .where(users.c.email == email)
            .values(
                cookie=cookie,
                cookie_expire_time=cookie_expire_time,
            )
        )
        user = await db.execute(query)
        return user

    @classmethod
    async def check_cookie(cls, cookie):
        query = users.select().where(users.c.cookie == cookie)
        user = await db.fetch_one(query)
        if user:
            if time.time() < dict(user)["cookie_expire_time"]:
                return dict(user)["email"]
        return None

    @classmethod
    async def delete_cookie(cls, cookie):
        query = (
            users.update()
            .where(users.c.cookie == cookie)
            .values(cookie=None, cookie_expire_time=None)
        )
        email = await db.execute(query)
        return email
