from sqlalchemy import Column, ForeignKey, Integer, Table, and_

from app.db import db, metadata

spaces = Table(
    "spaces",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("number", Integer, nullable=False),
    Column("start_x", Integer, nullable=False),
    Column("start_y", Integer, nullable=False),
    Column("end_x", Integer, nullable=False),
    Column("end_y", Integer, nullable=False),
    Column("car_id", Integer, ForeignKey("cars.id"), index=True),
    Column("zone_id", Integer, ForeignKey("zones.id"), index=True),
)


class Space:
    @classmethod
    async def get_free_spaces(cls, zone_id):
        query = spaces.select().where(
            and_(spaces.c.zone_id == zone_id, spaces.c.car_id == None)
        )
        free_spaces = await db.fetch_all(query)
        return free_spaces

    @classmethod
    async def get_spaces(cls, zone_id):
        query = spaces.select().where(and_(spaces.c.zone_id == zone_id))
        all_spaces = await db.fetch_all(query)
        return all_spaces

    @classmethod
    async def get_space(cls, id, zone_id):
        query = spaces.select().where(
            and_(spaces.c.id == id, spaces.c.zone_id == zone_id)
        )
        space = await db.fetch_one(query)
        return space

    @classmethod
    async def check_free_space(cls, id, zone_id):
        query = spaces.select().where(
            and_(
                spaces.c.id == id, spaces.c.zone_id == zone_id, spaces.c.car_id == None
            )
        )
        free_space = await db.fetch_one(query)
        return True if free_space else False

    @classmethod
    async def book_space(cls, id, zone_id, car_id):
        query = (
            spaces.update()
            .where(and_(spaces.c.id == id, spaces.c.zone_id == zone_id))
            .values(
                car_id=car_id,
            )
        )
        await db.execute(query)
        query = spaces.select().where(
            and_(
                spaces.c.id == id,
                spaces.c.zone_id == zone_id,
                spaces.c.car_id == car_id,
            )
        )
        booked_space = await db.fetch_one(query)
        return booked_space

    @classmethod
    async def release_space(cls, id, zone_id):
        query = (
            spaces.update()
            .where(and_(spaces.c.id == id, spaces.c.zone_id == zone_id))
            .values(
                car_id=None,
            )
        )
        await db.execute(query)
        query = spaces.select().where(
            and_(
                spaces.c.id == id, spaces.c.zone_id == zone_id, spaces.c.car_id == None
            )
        )
        released_space = await db.fetch_one(query)
        return released_space
