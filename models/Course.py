from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from models.ApplicantCourse import ApplicantCourse
from backend.Base import Base


class Course(Base):
    __tablename__ = 'courses'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    max_students_number = Column(Integer, default=0)
    name = Column(String, unique=True)
    link = Column(String, unique=True)
    applicants = relationship("Applicant", secondary=ApplicantCourse.__table__,
                              back_populates="courses")
    sorted = relationship("Sorted", back_populates="course")

    def __str__(self):
        return self.name
