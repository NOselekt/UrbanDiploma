## Overview
This service is a model of a small colledge with several courses. The site collects data from applicants with registration form, sorts them and shows the best applicants who chose given course.
## Installation
1. Copy repository
2. Install modules from requirements.txt with terminal or your package manager.
3. Create database. In this project I used PostgreSQL, you can choose another one of SQL-type. Next instructions are for PostgreSQL and pgAdmin.
4. In backend.async_database.py change engine declaration according to your database. Insert in the curly braces your data. 
Do the same to backend.database.py.
5. Insert in the terminal "alembic init migrations".
6. Paste env.py into migrations folder. Insert into config.set_section_option() functions your data.
7. Insert in the terminal "alembic revision --autogenerate -m "{paste your revision name}"
   Insert in the terminal "alembic upgrade head"
8. Add to the database your courses
## Usage
Insert into terminal "python -m uvicorn main:app" use the site. You can add applicant's data with registration form or check actual lists of applicants.