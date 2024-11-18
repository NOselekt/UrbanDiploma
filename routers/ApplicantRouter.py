from routers.__init__ import *

'''
The router for interaction with applicants
'''
templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/applicant", tags=["Applicant"])


@router.get("/registration")
async def registration(request: Request,
                       database: Annotated[AsyncSession, Depends(get_database)]) -> HTMLResponse:
    '''
    :param request: request
    :param database: database to work with
    :return: Template response with registration form and list of available courses
    '''

    try:
        courses = (await database.scalars(select(Course))).all()
    except Exception as e:
        raise HTTPException(status_code=503, detail="С базой данных произошла ошибка: " + str(e))

    courses_names = [course.name for course in courses]
    return templates.TemplateResponse("registration.html", {"request": request, "courses": courses_names})


@router.post("/registered")
async def registration(request: Request,
                       database: Annotated[AsyncSession, Depends(get_database)],
                       create_applicant: Annotated[CreateApplicant, Form()]) -> HTMLResponse:
    '''
    :param request: request
    :param database: database to work with
    :param create_applicant: HTML form with applicant data
    :return: template response with a button to return to the main page

    Gets applicant data from HTML form, validates it, and creates a new applicant in the database.
    '''

    new_attributes = {
        "snils": create_applicant.snils,
        "score": create_applicant.score,
        "olimp": create_applicant.olimp,
        "password": hashlib.sha384(create_applicant.password.encode()).hexdigest()
    }

    courses = [course for course in create_applicant.courses if course]

    if len(courses) != len(set(courses)):
        raise HTTPException(status_code=400, detail="Duplicate courses")

    try:
        new_applicant = Applicant(**new_attributes)
        for course_name in courses:
            course = await database.scalar(select(Course)
                                           .where(Course.name == course_name)
                                           .options(selectinload(Course.applicants), ))
            course.applicants.append(new_applicant)
            await database.execute(delete(Sorted))
        await database.commit()

    except Exception as e:

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return templates.TemplateResponse("registered.html", {"request": request})
