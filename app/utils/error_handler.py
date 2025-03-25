from functools import wraps
from sqlalchemy.exc import SQLAlchemyError

#this func fights excepticons
def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SQLAlchemyError as e:
            raise Exception(f"Database error {str(e)}")
        except Exception as e:
            raise Exception(f"Error in {func.__name__}: {str(e)}")
    return wrapper