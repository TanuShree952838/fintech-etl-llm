# src/database/models.py

from sqlalchemy import Column, Integer, String, Float, Date
from .db_connection import Base

class DataEntry(Base):
    __tablename__ = 'data_entries'
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    date = Column(Date)
    value = Column(Float)
