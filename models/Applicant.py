from sqlalchemy import Column, Integer, String, Boolean, BigInteger
from sqlalchemy.orm import relationship

from backend.Base import Base
from models.Course import Course
from models.ApplicantCourse import ApplicantCourse


class Applicant(Base):
    __tablename__ = 'applicants'
    __table_args__ = {'extend_existing': True}
    id = Column(BigInteger, primary_key=True, index=True)
    snils = Column(BigInteger, unique=True)
    score = Column(Integer)
    olimp = Column(Boolean, default=False)
    password = Column(String)
    courses = relationship("Course", secondary=ApplicantCourse.__table__,
                           back_populates="applicants")
    sorted = relationship("Sorted", uselist=False, back_populates="applicant")

    def __str__(self):
        return f"SNILS: {self.snils}, score: {self.score}"
