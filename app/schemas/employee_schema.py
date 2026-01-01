from pydantic import (
    BaseModel,
      EmailStr,
        Field,
          SecretStr,
            field_validator,
              ValidationError)
from typing import Optional , Annotated
from datetime import datetime
import re

class EmployeeBase(BaseModel):
    first_name: str = Field(..., min_length=2)
    last_name: str = Field(..., min_length=2)
    email: EmailStr
    department: str = Field(..., pattern= "^(HR|Sales|Engineering|Marketing|Finance|IT|Operations|Management|Support|Law|Medical)$")
    username: Annotated[Optional[str], Field(min_length=3, max_length=50)] = None # username must be between 3 and 50 characters long
    job_title: Optional[str] = None
    phone_number: Optional[str] = None

class EmployeeCreate(EmployeeBase):
    password: SecretStr = Field(..., min_length=8, max_length=72)# password is stored as a SecretStr to prevent accidental exposure in logs or error messages and hide its value when printed.

    @field_validator("password")
    def validate_password(cls, v: SecretStr) -> SecretStr:
        pwd = v.get_secret_value()
        if len(pwd) > 72:
            raise ValueError("Password must not exceed 72 characters.")
        if not re.search(r"[A-Z]", pwd):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", pwd):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"[0-9]",pwd):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", pwd):
            raise ValueError("Password must contain at least one special character.")
        return v


class EmployeeResponse(EmployeeBase):
    id: int
    display_name: str
    attendance_score: float
    is_active: bool
    created_at: datetime | None = None # If the user is verified, this field will contain the date and time of verification; otherwise, it will be None.

    class Config:
        from_attributes = True


# print(emp1.model_dump_json(indent=2)) # Test EmployeeBase model
from pydantic import ValidationError

try:
    emp = EmployeeCreate(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        department="Engineering",
        username="johndoe",
        password=SecretStr("MyoPass123#")  # Valid password
    )
    print("Created:", emp)
except ValidationError as e:
    print("Error:", e)


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
