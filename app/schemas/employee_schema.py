from pydantic import BaseModel, EmailStr, Field, SecretStr
from typing import Optional 
from datetime import datetime
from typing import Annotated

class EmployeeBase(BaseModel):
    first_name: str = Field(..., min_length=2)
    last_name: str = Field(..., min_length=2)
    email: EmailStr
    department: str = Field(..., pattern= "^(HR|Sales|Engineering|Marketing|Finance|IT|Operations|Management|Support|Law|Medical)$")
    username: Annotated[Optional[str], Field(min_length=3, max_length=50)] = None # username must be between 3 and 50 characters long
    job_title: Optional[str] = None
    phone_number: Optional[str] = None

class EmployeeCreate(EmployeeBase):
    password: SecretStr # password is stored as a SecretStr to prevent accidental exposure in logs or error messages and hide its value when printed.

class EmployeeResponse(EmployeeBase):
    id: int
    display_name: str
    attendance_score: float
    is_active: bool
    created_at: datetime | None = None # If the user is verified, this field will contain the date and time of verification; otherwise, it will be None.

    class Config:
        from_attributes = True

emp1 = EmployeeBase(
    first_name="John",
    last_name="Doe",
    email="joheahmed@gmail.com",
    department="hello",
    username="johndoe",
    job_title="Software Engineer",
    phone_number="123-456-7890"
)
# print(emp1.model_dump_json(indent=2)) # Test EmployeeBase model

# Frontend
#   |
#   |  (POST /register)
#   |  EmployeeCreate
#   ↓
# FastAPI
#   |
#   |  Validation (Pydantic)
#   ↓
# Business Logic
#   |
#   |  Hash password
#   |  Face encoding
#   |  Attendance score
#   ↓
# Database (SQLAlchemy Model)
#   |
#   ↓
# Response
#   |
#   |  EmployeeResponse
#   ↓
# Frontend
