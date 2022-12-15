from sqlalchemy import Column, Integer, Identity
from connections.orm_base import Base


class Key(Base):
    __tablename__ = "keys"
    id = Column('id', Integer, Identity(start=1, cycle=True), nullable=False, primary_key=True)
    hook_id = Column('hook_id', Integer, nullable=False)

    def __init__(self, hook_id: Integer):
        self.hook_id = hook_id
