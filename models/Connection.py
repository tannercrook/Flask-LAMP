from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session, query
from models.models import Base, metadata

engine = create_engine("postgresql+psycopg2://catalog_app:schoolrocks@localhost/course_catalog", implicit_returning=True)
engine.connect()

db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
Base.query = db_session.query_property()
