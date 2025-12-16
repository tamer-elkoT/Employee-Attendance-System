#This file reads the raw text from .env and converts it into usable Python variables.

import os
from dotenv import load_dotenv # Load environment variables from a .env file

load_dotenv() # load contents of the .env file into the environment

# Application Settings

class Settings:
    # Get the DB URL from the environment variable , if it's missing in .env, use a default value provided.
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./attendance.db")
    # Get tolerance. Crucially, wrap it in float() because environment variables are always strings of text.
    FACE_TOLRANCE: float = float(os.getenv("FACE_TOLERANCE",0.5))
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD",0.90))
    API_URL: str = os.getenv("API_URL", "http://127.0.0.1:8000/api")


settings = Settings()


