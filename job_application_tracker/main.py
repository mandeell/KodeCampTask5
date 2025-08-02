from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from models import JobApplication, JobApplicationCreate, Status
from file_handler import read_applications, write_applications

app = FastAPI()


def generate_id(application: JobApplicationCreate) -> str:
    return f"{application.name}_{application.company}_{application.position}".replace(" ", "_").lower()


@app.post("/applications")
async def create_application(application: JobApplicationCreate):
    applications = read_applications()
    app_id = generate_id(application)
    if app_id in applications:
        raise HTTPException(status_code=400, detail="Application already exists")

    app_data = JobApplication(**application.model_dump(), id=app_id)
    applications[app_id] = app_data.model_dump()
    write_applications(applications)
    return app_data


@app.get("/applications")
async def get_applications():
    applications = read_applications()
    return [JobApplication(**data) for data in applications.values()]


@app.get("/applications/search")
async def search_applications(status: Optional[Status] = Query(None)):
    applications = read_applications()
    if not status:
        return [JobApplication(**data) for data in applications.values()]
    return [
        JobApplication(**data)
        for data in applications.values()
        if data['status'].lower() == status.value.lower()
    ]