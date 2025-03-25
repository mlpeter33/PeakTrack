from sqlalchemy.orm import Session
from app.db.models import Period
from app.utils.error_handler import handle_exceptions
from datetime import datetime

@handle_exceptions
def create_period(db: Session, name: str, start_date: datetime, end_date: datetime, closed_by: int, auto_close: int, status: int):
    period = Period(name=name, start_date=start_date, end_date=end_date, closed_by=closed_by, auto_close=auto_close, status=status)
    db.add(period)
    db.commit()
    db.refresh(period)
    return period

@handle_exceptions
def get_period_by_id(db: Session, period_id: int):
    return db.query(Period).filter(Period.id == period_id).first()

@handle_exceptions
def get_all_periods(db: Session):
    return db.query(Period).all()

@handle_exceptions
def update_period_status(db: Session, period_id: int, status: int):
    period = db.query(Period).filter(Period.id == period_id).first()
    if period:
        period.status = status
        db.commit()
        db.refresh(period)
        return period