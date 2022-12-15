from sqlalchemy import Column, Integer, TIMESTAMP, Identity
from connections.orm_base import Base


class Loan(Base):
    __tablename__ = "loans"
    id = Column("id", Identity(start=1), primary_key=True, nullable=False)
    employee_id = Column("employee_id", Integer, nullable=False)
    key_id = Column("key_id", Integer, nullable=False)
    start_time = Column("start_time", TIMESTAMP, nullable=False)

    def __init__(self, employee_id: Integer, key_id: Integer, start_time: TIMESTAMP):
        self.employee_id = employee_id
        self.key_id = key_id
        self.start_time = start_time

