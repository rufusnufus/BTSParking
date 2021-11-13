from sqlalchemy import Column, Integer, String, Table

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
)


class Zone:
    @classmethod
    async def get_zone(cls, id):
        query = zones.select().where(zones.c.id == id)
        zone = await db.fetch_one(query)
        return zone

    @classmethod
    async def get_zones(cls):
        query = zones.select()
        existing_zones = await db.fetch_all(query)
        return existing_zones
