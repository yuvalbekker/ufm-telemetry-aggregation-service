from sqlalchemy import Column, VARCHAR, Float, Integer, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Metric(Base):
    __tablename__ = "metric"
    switch_id = Column(VARCHAR(255), primary_key=True, index=True, unique=True)
    bandwidth_usage = Column(Float)
    latency = Column(Float)
    packet_errors = Column(Integer)
    collection_time = Column(TIMESTAMP)
    timestamp = Column(TIMESTAMP, nullable=False, server_default=func.now())
