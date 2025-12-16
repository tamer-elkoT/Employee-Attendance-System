from app.core.database import engine, SessionLocal, Base
from app.models.employee import Employee
import datetime

def create_test_employee(name: str ,
                          department: str ,
                          encoding: bytes = b'\x00\x01\x02\x03',
                            last_seen: datetime.datetime = datetime.datetime.utcnow()):
    """
    Creates a new employee in the database.
    
    Parameters:
    - name (str): Employee's name
    - department (str): Employee's department
    - encoding (bytes): Facial encoding (default example bytes)
    
    Returns:
    - Employee object that was created
    """
    # Create the database tables
    Base.metadata.create_all(bind=engine) # bind the metadata to the engine to create tables
    # Create a new database session
    db = SessionLocal()
    try:
        # Create a new employee
        employee = Employee(
            name = name,
            department = department,
            encoding = encoding,  # Example binary data for facial encoding
            last_seen = last_seen
        )

        # Add the new employee to the session
        db.add(employee)
        # Commit the session to save the employee to the database
        db.commit()
        # Refresh the employee object with any new data from the database
        db.refresh(employee)
        print(f"Create Employee: {employee.name} with ID {employee.id} it's department is {employee.department}")
        return employee
    finally:
        # Close the database session
        db.close()
# Call the function to create a test employee
emp1 = create_test_employee("Tamer", "AI", b'\x10\x20\x30\x40') 
emp2 = create_test_employee("Alice", "HR", b'\x50\x60\x70\x80')

# Test print to verify creation
print(f"Test Employee 1: {emp1.name}, Department: {emp1.department}, ID: {emp1.id}")
print(f"Test Employee 2: {emp2.name}, Department: {emp2.department}, ID: {emp2.id}")

