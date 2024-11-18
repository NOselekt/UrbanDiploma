import time
import logging
from sqlalchemy import select, insert, delete
from sqlalchemy.orm import selectinload, Session

from models.Course import Course
from models.Applicant import Applicant
from models.Sorted import Sorted

''' A constant for counting the number of threads and processes.
Depends on the CPU'''
MAGIC_NUMBER = 16

'''A constant for the number of applicants in each course for random filling.'''
NUMBER_OF_APPLICANTS_IN_COURSE = 1000

'''A Set of symbols for random password generation.'''
SYMBOLS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-|/\\!@#%^&*()'

logging.basicConfig(level=logging.INFO, filemode="w", filename="fill_db.log", encoding='UTF-8',
                    format="%(levelname)s | %(message)s | %(asctime)s")
logging.basicConfig(level=logging.INFO, filemode="w", filename="fill_db.log", encoding='UTF-8',
                    format="%(levelname)s | %(message)s | %(asctime)s")
