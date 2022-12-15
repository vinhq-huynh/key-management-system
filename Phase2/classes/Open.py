from sqlalchemy import Column, Integer
from connections.orm_base import Base


class Open(Base):
    __tablename__ = "opens"
    hook_id = Column("hook_id", Integer, primary_key=True, nullable=False)
    door_id = Column("door_id", Integer, primary_key=True, nullable=False)

    def __init__(self, hook_id: Integer, door_id: Integer):
        self.hook_id = hook_id
        self.door_id = door_id
