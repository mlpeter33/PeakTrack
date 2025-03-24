from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    area_id = Column(Integer, ForeignKey("areas.id"))
    company_id = Column(Integer, ForeignKey("companies.id"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    status = Column(Integer, default=1)

    roles = relationship("UserRole", back_populates="user")
    area = relationship("Area", back_populates="users")
    company = relationship("Company", back_populates="users")
    results = relationship("Result", back_populates="user")


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    status = Column(Integer, default=1)

    users = relationship("UserRole", back_populates="role")
    permissions = relationship("RolePermission", back_populates="role")


class UserRole(Base):
    __tablename__ = "users_roles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role_id = Column(Integer, ForeignKey("roles.id"))
    created_at = Column(DateTime, server_default=func.now())
    status = Column(Integer, default=1)

    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="users")


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    status = Column(Integer, default=1)

    roles = relationship("RolePermission", back_populates="permission")


class RolePermission(Base):
    __tablename__ = "roles_permissions"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    permission_id = Column(Integer, ForeignKey("permissions.id"))
    created_at = Column(DateTime, server_default=func.now())
    status = Column(Integer, default=1)

    role = relationship("Role", back_populates="permissions")
    permission = relationship("Permission", back_populates="roles")


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    status = Column(Integer, default=1)

    evaluations_setup = relationship("PeriodCompanyAreaCompetency", back_populates="company")
    users = relationship("User", back_populates="company")


class Area(Base):
    __tablename__= "areas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    status = Column(Integer, default=1)

    evaluations_setup = relationship("PeriodCompanyAreaCompetency", back_populates="area")
    users = relationship("User", back_populates="area")


class Period(Base):
    __tablename__= "periods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    closed_by = Column(Integer, ForeignKey("users.id"))
    auto_close = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    status = Column(Integer, default=1)

    evaluations_setup = relationship("PeriodCompanyAreaCompetency", back_populates="period")
    closed_by_user = relationship("User")


class Competency(Base):
    __tablename__= "competencies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    status = Column(Integer, default=1)

    evaluations_setup = relationship("PeriodCompanyAreaCompetency", back_populates="competency")
    results = relationship("Result", back_populates="competency")


class PeriodCompanyAreaCompetency(Base):
    __tablename__= "periods_companies_areas_competencies"

    id = Column(Integer, primary_key=True, index=True)
    period_id = Column(Integer, ForeignKey("periods.id"))
    company_id = Column(Integer, ForeignKey("companies.id"))
    area_id = Column(Integer, ForeignKey("areas.id"))
    competency_id = Column(Integer, ForeignKey("competencies.id"))
    created_at = Column(DateTime, server_default=func.now())
    status = Column(Integer, default=1)

    period = relationship("Period", back_populates="evaluations_setup")
    company = relationship("Company", back_populates="evaluations_setup")
    area = relationship("Area", back_populates="evaluations_setup")
    competency = relationship("Competency", back_populates="evaluations_setup")


class Result(Base):
    __tablename__= "results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    competency_id = Column(Integer, ForeignKey("competencies.id"))
    result = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    status = Column(Integer, default=1)

    user = relationship("User", back_populates="results")
    competency = relationship("Competency", back_populates="results")