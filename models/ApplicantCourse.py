from sqlalchemy import Column, BigInteger, ForeignKey, UniqueConstraint

from backend.Base import Base

class ApplicantCourse(Base):
    __tablename__ = 'applicants_courses'
    __table_args__ = {'unique_constraints': (UniqueConstraint('applicant_id', 'course_id',
                                                              name="index_unique_applicant_course", ),)}
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    applicant_id = Column(BigInteger, ForeignKey('applicants.id'), nullable=False)
    course_id = Column(BigInteger, ForeignKey('courses.id'), nullable=False)
