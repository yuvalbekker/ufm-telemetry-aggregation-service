from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.metric import Metric, Base
from sqlalchemy.orm.exc import NoResultFound


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

def fetch_metric_value(session, switch_id: str, metric_name: str):
    """
    Fetch the latest value of a metric for a specific switch.
    Returns (value, timestamp) or raises NoResultFound if not found.
    """
    valid_metrics = {"bandwidth_usage", "latency", "packet_errors"}
    if metric_name not in valid_metrics:
        raise ValueError(f"Invalid metric_name: {metric_name}")

    metric_obj = (
        session.query(Metric)
        .filter(Metric.switch_id == switch_id)
        .order_by(Metric.timestamp.desc())
        .first()
    )
    if not metric_obj:
        raise NoResultFound(f"No metric found for switch_id {switch_id}")
    value = getattr(metric_obj, metric_name)
    return value, metric_obj.timestamp