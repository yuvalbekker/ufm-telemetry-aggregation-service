from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.metric import Metric, Base

def get_engine(db_url: str):
    engine = create_engine(db_url)
    return engine

def get_session_maker(engine):
    return sessionmaker(bind=engine)

def ensure_tables(engine):
    Base.metadata.create_all(engine)

def upsert_metrics(session, metrics):
    """
    metrics: list of Metric (SQLAlchemy model instances)
    """
    for db_metric in metrics:
        session.merge(db_metric)
    session.commit()
