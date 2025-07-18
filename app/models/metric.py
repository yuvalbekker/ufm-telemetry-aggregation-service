from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Metric(Base):
    __tablename__ = "metric"
    switch_id = Column(String, primary_key=True, index=True)
    bandwidth_usage = Column(Float)
    latency = Column(Float)
    packet_errors = Column(Integer)