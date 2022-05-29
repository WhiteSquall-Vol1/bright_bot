from sqlalchemy import Column, String, Integer, DateTime

from app import Base


class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    created = Column(DateTime)

