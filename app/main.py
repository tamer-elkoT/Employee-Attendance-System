from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.core.database import engine, get_db, Base
from app.models.employee import Employee
from app.controllers.auth_controller import router

app = FastAPI(title="Employee Attendance System")

# Setup the DB by autimatically creating the tables 
Base.metadata.create_all(bind=engine)
app.include_router(router)
