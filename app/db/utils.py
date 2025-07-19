from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.metric import Metric, Base
from sqlalchemy.orm.exc import NoResultFound
from app.schemas.list_metrics import MetricValueResponse
from app.common.types.valid_metrics import MetricName

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

def fetch_metric_value(session, switch_id: str, metric_name: MetricName):
    """
    Fetch the latest value of a metric for a specific switch.
    Returns (value, timestamp) or raises NoResultFound if not found.
    """
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

def fetch_metrics(
    session,
    metric_name: str,
    limit: int = 10,
    offset: int = 0
):
    """
    Fetch a paginated list of the latest metric values for all switches.
    Returns (list of MetricValueResponse, total number of unique switches).
    """
    # Total unique switches
    total = session.query(Metric.switch_id).distinct().count()

    # Latest timestamp per switch_id (subquery)
    subq = (
        session.query(
            Metric.switch_id,
            Metric.timestamp.label("max_ts")
        )
        .order_by(Metric.switch_id, Metric.timestamp.desc())
        .distinct(Metric.switch_id)
        .subquery()
    )

    results = (
        session.query(Metric)
        .join(subq, (Metric.switch_id == subq.c.switch_id) & (Metric.timestamp == subq.c.max_ts))
        .order_by(Metric.switch_id)
        .offset(offset)
        .limit(limit)
        .all()
    )

    # Convert to response objects
    response_items = [
        MetricValueResponse(
            switch_id=m.switch_id,
            value=getattr(m, metric_name),
            timestamp=m.timestamp
        )
        for m in results
    ]

    return response_items, total