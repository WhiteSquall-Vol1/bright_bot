from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import backref, relationship

from app import Base


class Answer(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    question_id = Column(Integer, ForeignKey('questions.id'))
    course = relationship("Question", backref=backref('answers'))
    created = Column(DateTime)
