from sqlalchemy import Column, String
from connections.orm_base import Base


class DoorName(Base):
    __tablename__ = "door_names"
    name = Column("name", String(20), primary_key=True, nullable=False)

    def __init__(self, name: String):
        self.name = name
