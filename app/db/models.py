from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

# fyi: status = 0 is inactive, status = 1 is active

# Switch server_default=func.now() to default=func.now() on dates 
# if you want SQLAlchemy to manage timestamps instead of the DB

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    area_id = Column(Integer, ForeignKey("areas.id"))
    company_id = Column(Integer, ForeignKey("companies.id"))
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    status = Column(Integer, default=1, nullable=False)

    roles = relationship("UserRole", back_populates="user")
    area = relationship("Area", back_populates="users")
    company = relationship("Company", back_populates="users")
    results = relationship("Result", back_populates="user")
    closed_periods = relationship("Period", back_populates="closed_by_user")


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    status = Column(Integer, default=1, nullable=False)

    users = relationship("UserRole", back_populates="role")
    permissions = relationship("RolePermission", back_populates="role")


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    status = Column(Integer, default=1, nullable=False)

    roles = relationship("RolePermission", back_populates="permission")


class Area(Base):
    __tablename__= "areas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    status = Column(Integer, default=1, nullable=False)

    users = relationship("User", back_populates="area")
    skills = relationship("AreaSkill", back_populates="area")
    companies = relationship("CompanyArea", back_populates="area")


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    status = Column(Integer, default=1, nullable=False)

    users = relationship("User", back_populates="company")
    areas = relationship("CompanyArea", back_populates="company")
    periods = relationship("PeriodCompany", back_populates="company")


class Period(Base):
    __tablename__= "periods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    closed_by = Column(Integer, ForeignKey("users.id"))
    auto_close = Column(Integer, default=0) #0 for no, 1 for yes
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    status = Column(Integer, default=1, nullable=False)

    closed_by_user = relationship("User", back_populates="closed_periods")
    companies = relationship("PeriodCompany", back_populates="period")


class Skill(Base):
    __tablename__= "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    type = Column(Integer, default=0) #0 for soft skills, 1 for technical skills
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    status = Column(Integer, default=1, nullable=False)

    areas = relationship("AreaSkill", back_populates="skill")
    results = relationship("Result", back_populates="skill")


class Result(Base):
    __tablename__= "results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    skill_id = Column(Integer, ForeignKey("skills.id"))
    score = Column(Numeric(5, 2))
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    status = Column(Integer, default=1, nullable=False)

    user = relationship("User", back_populates="results")
    skill = relationship("Skill", back_populates="results")


class UserRole(Base):
    __tablename__ = "users_roles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    status = Column(Integer, default=1, nullable=False)

    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="users")
    

class RolePermission(Base):
    __tablename__ = "roles_permissions"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    permission_id = Column(Integer, ForeignKey("permissions.id"))
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    status = Column(Integer, default=1, nullable=False)

    role = relationship("Role", back_populates="permissions")
    permission = relationship("Permission", back_populates="roles")


class AreaSkill(Base):
    __tablename__="areas_skills"

    id = Column(Integer, primary_key=True, index=True)
    area_id = Column(Integer, ForeignKey("areas.id"))
    skill_id = Column(Integer, ForeignKey("skills.id"))
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    status = Column(Integer, default=1, nullable=False)

    area = relationship("Area", back_populates="skills")
    skill = relationship("Skill", back_populates="area")

class CompanyArea(Base):
    __tablename__= "companies_areas"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    area_id = Column(Integer, ForeignKey("areas.id"))
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    status = Column(Integer, default=1, nullable=False)

    company = relationship("Company", back_populates="areas")
    area = relationship("Area", back_populates="companies")


class PeriodCompany(Base):
    __tablename__= "periods_companies"

    id = Column(Integer, primary_key=True, index=True)
    period_id = Column(Integer, ForeignKey("periods.id"))
    company_id = Column(Integer, ForeignKey("companies.id"))
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    status = Column(Integer, default=1, nullable=False)

    period = relationship("Period", back_populates="companies")
    company = relationship("Company", back_populates="periods")