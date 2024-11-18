from fastapi import status, HTTPException, Request, Form, APIRouter, Depends, Path
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from backend.async_database_depends import get_database
import hashlib
import os

from models.Course import Course
from models.Applicant import Applicant
from models.Sorted import Sorted
from schemas.CreateApplicant import CreateApplicant
from models.ApplicantCourse import ApplicantCourse
