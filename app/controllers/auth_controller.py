from fastapi import APIRouter, UploadFile, File, Form, Depends
# APIRouter : Used for creating an organized routes instead of using routes inside main.py
# UploadFile : To recieve the images files from the web
# File : To specify that this variable is File
# Form : Tor recieve form data like (name, department)
# Depends : Used for database session --> dependency injection
from sqlalchemy.orm import Session
from typing import List
from app.core import database
from app.models.employee import Employee
from app.services.face_logic import load_image_from_bytes, detect_faces, get_live_encoding, find_match

router = APIRouter(prefix="/api",
                   tags=["Authentication"])
# Endpoint 1 : Register 
@router.post("/register")
async def register(
    name: str = Form(...),
    department: str = Form(...),
    files: List[UploadFile] = File(...), # File is Required --> Waiting for request of images that will come from the webcam
    db: Session = Depends(database.get_db) # FastAPI Call get_db() --> open Session --> but the session in db variable 
    ):
    
    best_encoding_bytes, best_index, best_confidence = await detect_faces(files)

    if not best_encoding_bytes:
        return {"status": "error", "msg": "No clear face found."}
    # Add new Employee in Table Employee in the DataBase
    new_employee = Employee(
        name=name,
        department=department,
        encoding=best_encoding_bytes
    )
    
    # Add the info 
    db.add(new_employee)
    db.commit()
    # Refresh the db
    db.refresh(new_employee)
    return {"status": "success", "msg": f"Registered {name}"}

# Endpoint 2 : Recognize
@router.post("/recognize")
async def recognize(
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
):
    image_bytes= await file.read() # Read the image as bytes
    live_encoding = get_live_encoding(image_bytes) # Return encoding images using HOG detector
    if not live_encoding:
        return {"status": "error", "msg": "No clear face found."}
    
    # Get all the employees
    employees = db.query(Employee).all()

    # Compare between the known employees and live_encoding
    employee,_,distance = find_match(employees, live_encoding)

    if employee:
        return {"status": "success", "name": employee.name, "department":employee.department}
    else:
        return {"status": "error", "msg": "Uknown"}
    
    

