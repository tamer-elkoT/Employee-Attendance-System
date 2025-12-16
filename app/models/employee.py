from sqlalchemy import Column, Integer, String, LargeBinary, DateTime
from app.core.database import Base # Import the Base class from the database module
# The Base class is used to define the declarative models for SQLAlchemy
import datetime
# Define the Employee model class, inheriting from Base
class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True) # Primary key column for employee ID
    name = Column(String, index=True)
    department = Column(String, index=True)
    encoding = Column(LargeBinary) # Column to store the facial encoding as binary data
    last_seen = Column(DateTime, default=datetime.datetime.utcnow) # Column to store the last seen timestamp
    