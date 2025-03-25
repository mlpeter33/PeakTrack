from sqlalchemy.orm import Session
from app.db.models import Area, AreaSkill
from app.utils.error_handler import handle_exceptions

@handle_exceptions
def create_area(db: Session, name: str, description: str, status: int):
    area = Area(name=name, description=description, status=status)
    db.add(area)
    db.commit()
    db.refresh(area)
    return area

@handle_exceptions
def get_area_by_id(db: Session, area_id: int):
    return db.query(Area).filter(Area.id == area_id).first()

@handle_exceptions
def get_all_areas(db: Session):
    return db.query(Area).all()

@handle_exceptions
def update_area_status(db: Session, area_id: int, status: int):
    area = db.query(Area).filter(Area.id == area_id).firts()
    if area:
        area.status = status
        db.commit()
        db.refresh()
        return area

