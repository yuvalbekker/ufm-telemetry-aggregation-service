from app.core.config import settings
import app.db.utils as db_utils


def get_session():
    engine = db_utils.get_engine(settings.DB_URL)
    SessionLocal = db_utils.get_session_maker(engine)
    db_utils.ensure_tables(engine)
    with SessionLocal() as session:
        yield session
