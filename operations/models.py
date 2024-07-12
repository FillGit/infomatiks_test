from sqlalchemy import Column, DateTime, Integer, String
from database import Base


class Operation(Base):
    __tablename__ = 'operation'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    flight_number = Column(String(20), nullable=False)
    coordinatex = Column(String(20), nullable=False)
    coordinatey = Column(String(20), nullable=False)
    out_n = Column(String(20), nullable=False)
    coordinates_time = Column(DateTime())
    out_time = Column(DateTime())
    name_time = Column(String(20), nullable=False)

