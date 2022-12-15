from sqlalchemy import Column, String, Date, Integer
from connections.orm_base import Base


class AccessRequest(Base):
    __tablename__ = "access_requests"
    date = Column("date", Date, primary_key=True, nullable=False)
    room_number = Column("room_number", Integer, primary_key=True, nullable= False )
    building_name = Column("building_name", String(20), primary_key=True, nullable=False)
    employee_id = Column("employee_id", Integer, primary_key=True, nullable=False)

    def __init__(self, date: Date, room_number: Integer, building_name: String, employee_id: Integer):
        self.date = date
        self.room_number = room_number
        self.building_name = building_name
        self.employee_id = employee_id
