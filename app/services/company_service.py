from sqlalchemy.orm import Session
from app.db.models import Company
from app.utils.error_handler import handle_exceptions

@handle_exceptions
def create_company(db: Session, name: str, description: str, status: int):
    company = Company(name=name, description=description, status=status)
    db.add(company)
    db.commit()
    db.refresh(company)
    return company

@handle_exceptions
def get_company_by_id(db: Session, company_id: int):
    return db.query(Company).filter(Company.id == company_id).first()

@handle_exceptions
def get_all_companies(db: Session):
    return db.query(Company).all()

@handle_exceptions
def update_company_status(db: Session, company_id: int, status: int): 
    company = db.query(Company).filter(Company.id == company_id).first()
    if company: 
        company.status = status
        db.commit()
        db.refresh(company)
        return company