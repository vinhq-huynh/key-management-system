from sqlalchemy import Column, Integer, Date
from connections.orm_base import Base


class Loss(Base):
    __tablename__ = "losses"
    loan_id = Column("loan_id", Integer, primary_key=True, nullable=False)
    date = Column("date", Date, nullable=False)

    def __init__(self, loan_id: Integer, date: Date):
        self.loan_id = loan_id
        self.date = date
