from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
# APIRouter : Used for creating an organized routes instead of using routes inside main.py
# UploadFile : To recieve the images files from the web
# File : To specify that this variable is File
# Form : Tor recieve form data like (name, department)
# Depends : Used for database session --> dependency injection
from sqlalchemy.orm import Session, desc
from typing import List
from app.core import database, security
from app.models.employee import Employee, AttendanceLog
from app.services.face_logic import load_image_from_bytes, detect_faces, get_live_encoding, find_match
from app.schemas.employee_schema import EmployeeCreate
from app.services import score_logic
import json
# Create the APIRouter instance
# all endpoints will start with /api
router = APIRouter(prefix="/api",
                   tags=["Authentication"])
# Endpoint 1 : Register 
@router.post("/register")
async def register(
    employee_data: str = Form(...), # employee_data is a string in JSON format that comes from the form from the frontend entered by the user 
    files: List[UploadFile] = File(...), # File is Required --> Waiting for request of images that will come from the webcam
    db: Session = Depends(database.get_db) # FastAPI Call get_db() --> open Session --> but the session in db variable 
    ):
    try:
        data_dict = json.loads(employee_data) # Convert the JSON string to a Python dictionary
        valid_data = EmployeeCreate(**data_dict) # Validate and parse the data using Pydantic model to ensure it meets the required schema
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Validation Error: {str(e)}" )
    # Check Email is Unique in the database 
    if db.query(Employee).filter(Employee.email == valid_data.email).first(): 
        raise HTTPException(status_code=400, detail="Email already registered.")
    
    # Face Encoding from the uploaded images
    best_encoding_bytes, best_index, best_confidence = await detect_faces(files)

    if not best_encoding_bytes:
        return {"status": "error", "msg": "No Face Detected in Photos."}
    # Password Hashing
    pwd_hash = None
    if valid_data.password:
        pwd_hash = security.get_password_hash(valid_data.password)
    # Add new Employee in Table Employee in the DataBase
    new_employee = Employee(
        first_name=valid_data.first_name,
        last_name=valid_data.last_name,
        email=valid_data.email,
        department=valid_data.department,
        job_title=valid_data.job_title,
        phone_number=valid_data.phone_number,
        hashed_password=pwd_hash,
        encoding=best_encoding_bytes,
        attendance_score=100.0
    )
    
    # Add the info 
    db.add(new_employee)
    db.commit()
    # Refresh the db
    db.refresh(new_employee)
    return {"status": "success", "msg": f"Registered {valid_data.first_name} {valid_data.last_name} successfully."}

# Endpoint 2 : Recognize
@router.post("/recognize")
async def recognize(
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
):
    image_bytes= await file.read() # Read the image as bytes
    live_encoding = get_live_encoding(image_bytes) # Return encoding images using HOG detector
    if not live_encoding:
        return {"status": "error", "msg": "No Face Detected."}
    
    # Get all the employees
    employees = db.query(Employee).all()

    # Compare between the known employees and live_encoding
    employee,_,distance = find_match(employees, live_encoding)

    if employee:
        # Mark Attendance to get the status (On Time / Late) and update the attendance score if Late
        status, new_score = score_logic.mark_attendance(db, employee.id )

        return {
            "status": "success",
              "name": employee.display_name,
                "department":employee.department,
                "attendance_score": new_score,
                "attendance_status": status}
    else:
        return {"status": "Unknown"}
    
# Endpoint 3 : Get Employees_id
@router.get("/history/{employee_id}")
def get_history(employee_id: int, skip: int =0, limit: int = 10, dp: Session = Depends(database.get_db)):
    """Get attendance history for a specific employee."""
    # Starts a query on the Employee table to find the employee with the given employee_id
    emp = db.query(Employee).filter(Employee.id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found.")
    # Query the AttendanceLog table to get attendance records for the specified employee
    # db.query(AttendanceLog) → Start a query on the AttendanceLog table.
    # .filter(AttendanceLog.employee_id == emp.id) → Only select logs for this employee.
    #  .offset(skip) → Skip the first skip logs.
    # .limit(limit) → Limit the number of logs returned. Default is 10.
    # all() → Return all rows matching the query as a list of AttendanceLog objects.
    attendance_logs = (
        db.query(AttendanceLog).filter(AttendanceLog.employee_id == emp.id)\
        .order_by(desc(AttendanceLog.timestamp)).offset(skip).limit(limit).all()
        
    )
    
    logs_formatted = [
        {
            "date":log.timestamp.strftime("%Y-%m-%d"),
            "time":log.timestamp.strftime("%H:%M %p"),
            "status":log.status
        }
        for log in attendance_logs

    ]

    return {
        "employee": {"id": emp.id, "name":emp.display_name, "department": emp.department},
        "attendance_logs": logs_formatted
    }