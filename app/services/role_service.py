from sqlalchemy.orm import Session
from app.db.models import Role, RolePermission
from app.utils.error_handler import handle_exceptions

@handle_exceptions
def create_role(db: Session, name: str, description: str):
    role = Role(name=name, description=description)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

@handle_exceptions
def get_role_by_id(db: Session, role_id: int):
    return db.query(Role).filter(Role.id == role_id).first()

@handle_exceptions
def get_all_roles(db: Session):
    return db.query(Role).all()

@handle_exceptions
def update_role_status(db: Session, role_id: int, status: int = 1):
    role = db.query(Role).filter(Role.id == role_id).first()
    if role:
        role.status = status
        db.commit()
        db.refresh(role)
        return role
    
@handle_exceptions
def add_permission(db: Session, role_id: int, permission_id: int, status: int):
    existing_permission = db.query(RolePermission).filter(
        RolePermission.role_id == role_id,
        RolePermission.permission_id == permission_id
    ).first()

    if existing_permission:
        return existing_permission
    
    role_permission = RolePermission(role_id=role_id, permission_id=permission_id, status=status)
    db.add(role_permission)
    db.commit
    db.refresh(role_permission)
    return role_permission