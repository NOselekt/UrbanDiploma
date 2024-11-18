from typing import Annotated
from fastapi import Depends
import threading as ted
import random as rand

from backend.database_depends import get_database
from backend.__init__ import *


def add_courses(database: Annotated[Session, Depends(get_database)]):
    '''
    :param database: database to wotk with
    :return: None
    Adds some courses to the database. Use for testing, if you are too lazy to add them yourself.
    '''
    database.execute(insert(Course).values(name="Информационная безопасность",
                                           max_students_number=35,
                                           link="is"))
    database.execute(insert(Course).values(name="Информатика и вычислительная техника",
                                           max_students_number=30,
                                           link="csch"))
    database.execute(insert(Course).values(name="Программная инженерия",
                                           max_students_number=20,
                                           link="pi"))
    database.execute(insert(Course).values(name="Биоинженерия и биоинформатика",
                                           max_students_number=10,
                                           link="bb"))
    database.execute(insert(Course).values(name="Математика и компьютерные науки",
                                           max_students_number=100,
                                           link="mcs"))
    database.execute(insert(Course).values(name="Прикладные математика и физика",
                                           max_students_number=70,
                                           link="amph"))
    database.execute(insert(Course).values(name="Фундаментальная и прикладная физика",
                                           max_students_number=60,
                                           link="faph"))
    database.execute(insert(Course).values(name="Прикладная информатика",
                                           max_students_number=50,
                                           link="acs"))
    database.execute(insert(Course).values(name="Прикладная математика",
                                           max_students_number=45,
                                           link="am"))
    database.execute(insert(Course).values(name="Прикладная математика и информатика",
                                           max_students_number=40,
                                           link="amcs"))


def fill_course_with_random(database: Annotated[Session, Depends(get_database)],
                            courses: list[Course]):
    '''
    :param database: database to work with
    :param courses: courses to fill
    :return: None

    For every course in the list creates a NUMBER_OF_APPLICANTS_IN_COURSE
    random applicants and inserts them into the database.
    '''
    for course in courses:
        for _ in range(NUMBER_OF_APPLICANTS_IN_COURSE):
            try:
                applicant = Applicant(snils=rand.randint(10 ** 10, 10 ** 11),
                                      score=rand.randint(100, 321),
                                      olimp=rand.choice([True, False]),
                                      password=rand.choice(SYMBOLS) * MAGIC_NUMBER)
                course.applicants.append(applicant)
                logging.info(f"Applicant {applicant.snils} added to course {course.name}")
            except Exception as e:
                logging.error(f"Failed adding applicant {applicant.snils} to course {course.name}: {e}")


def fill_db_with_random(database: Annotated[Session, Depends(get_database)]):
    '''
    :param database: datavase to work with
    :return: None

    Fills all courses in the database with random applicants.
     courses_number is a number of courses function got.
     courses_number_in_thread is a number of courses thread has to handle.
     threads_number is a number of threads that will be used to fill database.
     index_end is an index of the first course to be handled by the next thread.
    '''

    courses = database.scalars(select(Course).options(selectinload(Course.applicants), )).all()

    courses_number = len(courses)

    courses_number_in_thread = courses_number // MAGIC_NUMBER + 1

    threads_number = courses_number // courses_number_in_thread if courses_number % 2 == 0 \
        else courses_number // courses_number_in_thread + 1

    for i in range(0, threads_number, courses_number_in_thread):
        if i + courses_number_in_thread <= threads_number:
            index_end = i + courses_number_in_thread
        else:
            index_end = threads_number
        t = ted.Thread(target=fill_course_with_random,
                       args=(database,
                             courses[i:index_end]))
        t.start()
        t.join()


def fill_sorted_course(database: Annotated[Session, Depends(get_database)],
                       applicants: list[list[Applicant]], courses_ids: list[int]):
    '''
    :param database: database to work with
    :param applicants: list of lists where each inner list is sorted applicants
    :param courses_ids: ids of courses to fill
    :return: None

    For every course in the list insert in the separate table sorted applicants
    with specified id of the course.
    '''

    courses_number = len(courses_ids)

    for i in range(courses_number):
        for applicant in applicants[i]:
            try:
                database.execute(insert(Sorted).values(applicant_snils=applicant.snils,
                                                       applicant_score=applicant.score,
                                                       applicant_olimp=applicant.olimp,
                                                       course_id=courses_ids[i]))
            except Exception as e:
                logging.error(f"Failed adding applicant {applicant.snils} to course {courses_ids[i]}: {e}")


def fill_sorted(database: Annotated[Session, Depends(get_database)], applicants: list[list[Applicant]]):
    '''

    :param database: database to work with
    :param applicants: list of lists where each inner list is sorted applicants
    from courses_sort() function
    :return: None

    Fills table for sorted applicants with sorted applicants using threads
    courses_number is a number of courses function got.
     courses_number_in_thread is a number of courses thread has to handle.
     threads_number is a number of threads that will be used to fill database.
     index_end is an index of the first course to be handled by the next thread.
    '''

    courses_number = len(applicants)
    courses_number_in_thread = courses_number // MAGIC_NUMBER + 1
    threads_number = courses_number // courses_number_in_thread if courses_number % 2 == 0 \
        else courses_number // courses_number_in_thread + 1

    database.execute(delete(Sorted))

    for i in range(0, threads_number, courses_number_in_thread):
        if i + courses_number_in_thread <= threads_number:
            index_end = i + courses_number_in_thread
        else:
            index_end = threads_number
        t = ted.Thread(target=fill_sorted_course,
                       args=(database,
                             applicants[i:index_end],
                             list(range(i + 1, index_end + 1)),))
        t.start()
        t.join()

    database.commit()


if __name__ == "__main__":
    '''
    When the code is executed it fills the database with random applicants.
    '''
    from backend.database import engine

    with Session(engine) as database:
        # add_courses(database)

        courses = database.scalars(select(Course).options(selectinload(Course.applicants), )).all()

        fill_db_with_random(database)

        database.commit()