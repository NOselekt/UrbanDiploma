from routers.__init__ import *

'''The router for sending sorted table of applicants of the requested course.'''

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/result", tags=["Sorted"])


@router.get("/{link}")
async def result(request: Request,
                 database: Annotated[AsyncSession, Depends(get_database)],
                 link: str = Path(description="course link")) -> HTMLResponse:
    '''
    :param request: request
    :param database: database to work with
    :param link: link to the requested course
    :return: template response with sorted list of applicants of the requested course

    Gets link of one of the courses, get its data from database and sends
    sorted list of applicants on this course.
    '''

    try:

        course = await database.scalar(select(Course).where(Course.link == link))
        result = (await database.scalars(select(Sorted).where(Sorted.course_id == course.id))).all()

        if not result:
            os.system('python -m backend.course_sort')
            result = (await database.scalars(select(Sorted).where(Sorted.course_id == course.id))).all()
    except Exception as e:
        raise HTTPException(status_code=503, detail="С базой данных произошла ошибка: " + str(e))

    return templates.TemplateResponse("result.html", {"request": request, "course": course,
                                                      "result": result})
