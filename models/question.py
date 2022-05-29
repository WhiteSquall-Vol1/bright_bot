from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import backref, relationship

from app import Base


class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    number = Column(Integer, nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'))
    course = relationship("Course", backref=backref('questions'))
    created = Column(DateTime)
