from sqlalchemy import create_engine, Column, Integer, String, Text, Date, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import date

from config import settings


DATABASE_URL = settings.DB_URL
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=True)
    created_at = Column(Date, default=date.today)
    updated_at = Column(Date, default=date.today, onupdate=date.today)
    project_places = relationship("ProjectPlace", back_populates="project")


class Place(Base):
    __tablenname__ = "places"
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(Integer, unique=True, nullable=False)
    title = Column(String, nullable=False)
    api_data = Column(Text, nullable=True)
    created_at = Column(Date, default=date.today)

    project_places = relationship("ProjectPlace", back_populates="place")


class ProjectPlace(Base):
    __tablename__ = "project_places"
    project_id = Column(Integer, ForeignKey("projects.id"), primary_key=True)
    place_id = Column(Integer, ForeignKey("places.id"), primary_key=True)
    notes = Column(Text, nullable=True)
    visited = Column(Boolean, default=False)
    added_at = Column(Date, default=date.today)
    updated_at = Column(Date, default=date.today, onupdate=date.today)

    project = relationship("Project", back_populates="project_places")
    place = relationship("Place", back_populates="project_places")


Base.metadata.create_all(bind=engine)
