from datetime import datetime, timedelta, time
from sqlalchemy.orm import Session
from app.models.employee import Employee, AttendanceLog

# Official work start time (9:00 AM)
WORK_START_TIME = time(9, 0, 0)
# Allowed delay buffer in minutes
ALLOWED_DELAY_MINUTES = 15
# Score deduced if employee is late
LATE_PENALTY = 5.0

def mark_attendance(db: Session, employee_id: int):
    """
    Marks attendance for a given employee and updates their attendance score.

    Steps:
    1. Get current time
    2. Validate employee existence
    3. Calculate allowed late threshold
    4. Determine attendance status
    5. Update attendance score if late
    6. Save attendance log to database
    """

    # Capture Current Date and time 
    now = datetime.now()
    # Check if employee exists in the database by searching with employee_id
    emp = db.query(Employee).filter(Employee.id == employee_id).first() 
    # If employee does not exist, raise an error
    if not emp:
        raise ValueError("Employee not found.")
    # Calculate the allowed late threshold time
    # Example:
    # now.date() → 2026-01-02
    # WORK_START_TIME → 09:00:00
    #
    # Result:
    # datetime(2026-01-02 09:00:00)
    #
    # Then add late_penalty (5 minutes)
    # Final late time → 09:05:00
    late_time = (
        datetime.combine(now.date(), WORK_START_TIME) 
        + timedelta(minutes=ALLOWED_DELAY_MINUTES)
    ).time() 

    # Determine attendance status based on current time and late threshold

    if now.time() <= late_time:
        status = "On Time"
    else:
        status = "Late"
        # Deduct attendance score for being late
        emp.attendance_score = max(0.0, emp.attendance_score - LATE_PENALTY)

    # Create a new attendance log entry
    attendance_log = AttendanceLog(
        employee_id=employee_id,
        timestamp=now,
        status=status
    )
    try:
        # Save the attendance log and employee to the database
        db.add_all([emp, attendance_log])
        # Commit the transaction to database
        db.commit()
    
    except Exception:
        db.rollback()
        raise


    return status, emp.attendance_score

