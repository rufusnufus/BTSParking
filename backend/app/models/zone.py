from sqlalchemy import Column, Integer, String, Table, select

from app.db import db, metadata

zones = Table(
    "zones",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String(1), nullable=False, index=True),
    Column("start_x", Integer, nullable=False),
    Column("start_y", Integer, nullable=False),
    Column("end_x", Integer, nullable=False),
    Column("end_y", Integer, nullable=False),
    Column("hourly_rate", Integer, nullable=False),
)


class Zone:
    @classmethod
    async def get_zone(cls, id):
        query = zones.select().where(zones.c.id == id)
        zone = await db.fetch_one(query)
        return zone

    @classmethod
    async def get_hourly_rate_by_zone(cls, id):
        query = select(zones.c.hourly_rate).where(zones.c.id == id)
        hourly_rate = await db.fetch_one(query)
        return hourly_rate['hourly_rate']

    @classmethod
    async def get_width_height(cls, id):
        query = zones.select().where(zones.c.id == id)
        zone = await db.fetch_one(query)
        if zone:
            z = dict(zone)
            return (z["end_x"] - z["start_x"] + 1, z["end_y"] - z["start_y"] + 1)
        return None

    @classmethod
    async def get_zones(cls):
        query = zones.select()
        existing_zones = await db.fetch_all(query)
        return existing_zones
