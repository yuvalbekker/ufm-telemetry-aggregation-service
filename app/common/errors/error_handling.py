from functools import wraps
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from sqlalchemy.orm.exc import NoResultFound
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)

def db_error_handling(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found."
            )
        except (OperationalError, SQLAlchemyError) as ex:
            logger.error(f"Database error: {str(ex)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database is unavailable or query failed. Please try again later."
            )
        except Exception as ex:
            logger.error(f"Unexpected error: {str(ex)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred."
            )
    return wrapper
