from app.core.database import SessionLocal, engine
from app.models.employee import Employee, AttendanceLog
from sqlalchemy import text

def reset_database():
    db = SessionLocal()
    try:
        print("🗑️  Cleaning up database...")

        # 1. Delete all Attendance Logs first (Child table)
        num_logs = db.query(AttendanceLog).delete()
        print(f"   - Deleted {num_logs} attendance records.")

        # 2. Delete all Employees (Parent table)
        num_emps = db.query(Employee).delete()
        print(f"   - Deleted {num_emps} employees.")

        # 3. Reset ID Counters (Auto-increment) to 1
        # This is specific for PostgreSQL. If you are on SQLite, this block is skipped.
        try:
            db.execute(text("ALTER SEQUENCE employees_id_seq RESTART WITH 1"))
            db.execute(text("ALTER SEQUENCE attendance_logs_id_seq RESTART WITH 1"))
            print("   - ID counters reset to 1.")
        except Exception:
            pass # Fails silently on SQLite, which is fine.

        db.commit()
        print("✅ Database is now empty and ready for new users!")

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    reset_database()