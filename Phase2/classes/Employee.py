from sqlalchemy import Column, String, Integer, Identity
from connections.orm_base import Base


class Employee(Base):
    __tablename__ = "employees"
    id = Column('id', Integer, Identity(start=1, cycle=True), nullable=False, primary_key=True)
    name = Column("name", String(40), nullable=False)

    def __init__(self, name: String):
        self.name = name


