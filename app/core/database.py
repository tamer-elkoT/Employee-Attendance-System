from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Create the SQLAlchemy engine using the database URL from settings
# The connect_args parameter is used here to allow SQLite to be used in a multi-threaded environment.
# For other databases, this parameter may not be necessary.
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
# Create a configured "Session" class
# This class will be used to create new database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Create a base class for declarative class definitions
# This base class will be used to define the database models
Base = declarative_base()

# Dependency function to get a database session
# This function can be used with FastAPI's dependency injection system
# It ensures that the database session is properly created and closed after use
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
