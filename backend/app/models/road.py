from sqlalchemy import Column, ForeignKey, Integer, Table

from app.db import db, metadata

roads = Table(
    "roads",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("start_x", Integer, nullable=False),
    Column("start_y", Integer, nullable=False),
    Column("end_x", Integer, nullable=False),
    Column("end_y", Integer, nullable=False),
    Column("zone_id", Integer, ForeignKey("zones.id"), index=True),
)


class Road:
    @classmethod
    async def get_roads(cls, zone_id):
        query = roads.select().where(roads.c.zone_id == zone_id)
        roads_in_zone = await db.fetch_all(query)
        return roads_in_zone
