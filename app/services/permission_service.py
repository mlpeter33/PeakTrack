from sqlalchemy.orm import Session
from app.db.models import Permission
from app.utils.error_handler import handle_exceptions

@handle_exceptions
def get_permission_by_id(db: Session, permission_id: int):
    return db.query.filter(Permission.id == permission_id).first()

@handle_exceptions
def get_all_permissions(db: Session):
    return db.query(Permission).all()