from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from connections.orm_base import Base


class Room(Base):
    __tablename__ = "rooms"
    building_name = Column("building_name", String(20), ForeignKey("buildings.name"), primary_key=True, nullable=False)
    number = Column("number", Integer, primary_key=True, nullable=False)

    def __init__(self, building_name: String, number: Integer):
        self.building_name = building_name
        self.number = number
