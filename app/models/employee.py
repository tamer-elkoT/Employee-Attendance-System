from sqlalchemy import (
    Column,
      Integer,
        String,
          LargeBinary,
            DateTime, 
            ForeignKey,
            Float,
            Boolean)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base # Import the Base class from the database module
# The Base class is used to define the declarative models for SQLAlchemy
import datetime
# Define the Employee model class, inheriting from Base
class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True) # Primary key column for employee ID
    # Identitiy
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    department = Column(String, nullable=False)
    job_title = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    username = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=True)

    # Biometric Data
    encoding = Column(LargeBinary) # Column to store the facial encoding as binary data
    # Metrics
    attendance_score = Column(Float, default=100.0) # Column to store the attendance score, default is 100.0
    # Meta data
    is_active = Column(Boolean, default=True) # Column to indicate if the employee is active

    created_at = Column(DateTime, default=datetime.now) # Column to store the last seen timestamp
    
    # Relationship to Attendance records
    attendance_logs = relationship("Attendance", back_populates="employee")

    @property 
    def display_name(self) -> str:
        """Return the full name of the employee."""
        return f"{self.first_name} {self.last_name}"
    
class AttendanceLog(Base):
    __tablename__ = "attendance_logs"

    id = Column(Integer, primary_key=True, index=True) # Primary key column for attendance log ID
    employee_id = Column(Integer, ForeignKey("employees.id")) # Foreign key to link to the Employee model and store the employee ID
    # The ForeignKey is a reference to the employees table's id column
    # primary key is a unique identifier for each employee in the table
    timestamp = Column(DateTime, default=datetime.now) # Column to store the timestamp of the attendance log
    status = Column(String, default="On Time") # Column to store the attendance status (e.g., On Time, Late, Absent)

    # Relationship back to Employee
    employee = relationship("Employee", back_populates="attendance_logs")
    