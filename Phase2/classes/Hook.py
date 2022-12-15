from sqlalchemy import Column, Integer, Identity
from connections.orm_base import Base


class Hook(Base):
    __tablename__ = "hooks"
    id = Column('id', Integer, Identity(start=1, cycle=True), nullable=False, primary_key=True)
