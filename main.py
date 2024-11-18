from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pathlib import Path
from typing import Annotated

from backend.async_database_depends import get_database
from models.Course import Course
from routers import ApplicantRouter, ResultRouter

'''Main application code'''
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent / "static"),
    name="static",
)


@app.get("/")
async def main(request: Request,
               database: Annotated[AsyncSession, Depends(get_database)]) -> HTMLResponse:
    '''
    :param request: request
    :param database: database to work with
    :return: HTML response with main page and list of available courses

    Looking for available courses and sends them on the main page
    '''
    try:
        courses = await database.scalars(select(Course).order_by(Course.id))
    except Exception as e:
        raise HTTPException(status_code=503, detail="С базой данных произошла ошибка: " + str(e))

    return templates.TemplateResponse("main.html", {"request": request,
                                                    "courses": courses})


app.include_router(ResultRouter.router)
app.include_router(ApplicantRouter.router)
