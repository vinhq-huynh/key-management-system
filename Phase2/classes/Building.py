from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from connections.orm_base import Base


class Building(Base):
    __tablename__ = "buildings"
    name = Column("name", String(20), primary_key=True, nullable=False)

    def __init__(self, name: String):
        self.name = name
