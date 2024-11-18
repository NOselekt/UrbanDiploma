import multiprocessing as mup

from backend.fill_db import fill_sorted
from backend.__init__ import *


def quicksort(array: list[Applicant]) -> list[Applicant]:
    '''Simple quicksort function that gets list of applicants
    and returns list of applicants sorted by score in descending order'''
    if len(array) <= 1:
        return array
    else:
        pivot = array[0]
        left = [x for x in array[1:] if x.score > pivot.score]
        right = [x for x in array[1:] if x.score <= pivot.score]
        return quicksort(left) + [pivot] + quicksort(right)


def course_sort(courses: list[Course]) -> list[list[Applicant]]:
    '''Gets course object and returns list of its applicants
    sorted by next rules:
    1. Sorts applicants by score in descending order
    2. Adds to returning result of applicants
    who have Olimpic diploma and highest score among olympians
    in quantity of 10% of max number of students
    3. Adds applicants with highest score among non-olimpians
    till max number of students is reached'''
    result = []
    for course in courses:

        sorted_applicants = quicksort(course.applicants)

        applicants = []

        i = 0

        for applicant in sorted_applicants:
            if applicant.olimp:
                applicants.append(applicant)
                i += 1
                if i >= course.max_students_number // 10 + 1:
                    break

        for applicant in sorted_applicants:
            if not applicant.olimp:
                applicants.append(applicant)
                i += 1
                if i >= course.max_students_number:
                    break
        result.append(applicants)

    return result


def courses_sort(courses: list[Course]) -> list[list[Applicant]]:
    '''
    :param courses (list[Course]): list of courses that have applicants to sort.
    :return list[list[Applicant]]: list of lists where each inner list is sorted applicants.

    courses_number is a number of courses function got.
    courses_number_in_process is a number of courses process has to handle.
    processes_number is a number of processes that will be used to sort courses.
    '''

    courses_number = len(courses)

    courses_number_in_process = courses_number // MAGIC_NUMBER + 1

    processes_number = courses_number // courses_number_in_process if courses_number % 2 == 0 \
        else courses_number // courses_number_in_process + 1

    sorted_courses = []

    for i in range(0, processes_number, courses_number_in_process):
        if i + courses_number_in_process <= processes_number:
            index_end = i + courses_number_in_process
        else:
            index_end = processes_number
        sorted_courses.append(courses[i:index_end])

    with mup.Pool(processes_number) as pool:
        sorted_applicants = pool.map(course_sort, sorted_courses)

    result = []

    for new_courses in sorted_applicants:
        for course in new_courses:
            result.append(course)

    return result


if __name__ == "__main__":
    '''
    When the code is executed, it starts the sorting process using multiprocessing, 
    and then fills the sorted table with the sorted data.
    '''
    from backend.database import engine

    with Session(engine) as database:

        courses = database.scalars(select(Course).options(selectinload(Course.applicants)).order_by(Course.id)).all()

        applicants = courses_sort(courses)

        fill_sorted(database, applicants)

        database.commit()
