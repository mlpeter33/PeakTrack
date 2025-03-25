from sqlalchemy.orm import Session
from app.db.models import User, UserRole
from app.utils.error_handler import handle_exceptions

@handle_exceptions
def create_user(db: Session, name: str, email: str, area_id: int, company_id: int):
    user = User(name=name, email=email, area_id=area_id, company_id=company_id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@handle_exceptions
def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


@handle_exceptions
def get_all_users(db: Session):
    return db.query(User).all()


@handle_exceptions
def update_user_status(db: Session, user_id: int, status: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.status = status
        db.commit()
        db.refresh(user)
    return user

@handle_exceptions
def add_role(db: Session, user_id: int, role_id: int, status: int):
    existing_role = db.query(UserRole).filter(
        UserRole.user_id == user_id,
        UserRole.role_id == role_id
    ).first()

    if existing_role: 
        return existing_role

    user_role = UserRole(user_id=user_id, role_id=role_id, status=status)
    db.add(user_role)
    db.commit()
    db.refresh(user_role)
    return user_role
