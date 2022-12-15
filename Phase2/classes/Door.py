from sqlalchemy import Column, String, Integer, Identity, ForeignKey
from sqlalchemy.orm import relationship
from connections.orm_base import Base


class Door(Base):
    __tablename__ = "doors"
    id = Column('id', Integer, Identity(start=1, cycle=True), nullable=False, primary_key=True)
    building_name = Column("building_name", String(20), ForeignKey("rooms.building_name"), nullable=False)
    room_number = Column("room_number", Integer, ForeignKey("rooms.number"), nullable=False)
    door_name = Column("door_name", String(10), nullable=False)

    def __init__(self, building_name: String, room_number: Integer, door_name: String):
        self.building_name = building_name
        self.room_number = room_number
        self.door_name = door_name
