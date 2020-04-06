# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class CatalogYear(Base):
    __tablename__ = 'catalog_year'

    catalog_year_id = Column(Integer, primary_key=True, server_default=text("nextval('catalog_year_catalog_year_id_seq'::regclass)"))
    name = Column(String(30), nullable=False)
    endyear = Column(Integer, nullable=False)
    active = Column(Integer, nullable=False, server_default=text("1"))


class CreditType(Base):
    __tablename__ = 'credit_type'

    credit_type_id = Column(Integer, primary_key=True, server_default=text("nextval('credit_type_credit_type_id_seq'::regclass)"))
    name = Column(String(30), nullable=False)
    code = Column(String(6), nullable=False)


class School(Base):
    __tablename__ = 'school'

    school_id = Column(Integer, primary_key=True, server_default=text("nextval('school_school_id_seq'::regclass)"))
    number = Column(Integer, nullable=False)
    name = Column(String(60), nullable=False)
    abbreviation = Column(String(6), nullable=False)
    active = Column(Integer, nullable=False, server_default=text("1"))


class SystemUser(Base):
    __tablename__ = 'system_user'

    system_user_id = Column(Integer, primary_key=True, server_default=text("nextval('system_user_system_user_id_seq'::regclass)"))
    email = Column(String(60), nullable=False)
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    password = Column(String(250))
    salt = Column(String(250))


class Catalog(Base):
    __tablename__ = 'catalog'

    catalog_id = Column(Integer, primary_key=True, server_default=text("nextval('catalog_catalog_id_seq'::regclass)"))
    school_id = Column(ForeignKey('school.school_id'), nullable=False)
    catalog_year_id = Column(ForeignKey('catalog_year.catalog_year_id'), nullable=False)
    name = Column(String(30), nullable=False)

    catalog_year = relationship('CatalogYear')
    school = relationship('School')


class Course(Base):
    __tablename__ = 'course'

    course_id = Column(Integer, primary_key=True, server_default=text("nextval('course_course_id_seq'::regclass)"))
    catalog_id = Column(ForeignKey('catalog.catalog_id'), nullable=False)
    number = Column(String(20), nullable=False)
    name = Column(String(60), nullable=False)
    description = Column(Text)
    video_link = Column(String(250))
    credits = Column(Numeric)
    credit_type_id = Column(ForeignKey('credit_type.credit_type_id'))
    active = Column(Integer, nullable=False, server_default=text("1"))

    catalog = relationship('Catalog')
    credit_type = relationship('CreditType')
