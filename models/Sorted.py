from sqlalchemy import Column, Integer, String, Boolean, BigInteger, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from backend.Base import Base


class Sorted(Base):
    __tablename__ = 'sorted'
    __table_args__ = {'extend_existing': True}
    id = Column(BigInteger, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey('courses.id'))
    applicant_snils = Column(BigInteger, ForeignKey('applicants.snils'))
    course = relationship("Course", back_populates="sorted")
    applicant = relationship("Applicant", back_populates="sorted")
    applicant_score = Column(Integer)
    applicant_olimp = Column(Boolean)
