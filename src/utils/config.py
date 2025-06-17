import os
from pathlib import Path
from dotenv import load_dotenv
import psycopg2

# ===============================================
# Load Environment Variables from .env (Project Root)
# ===============================================
env_path = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(dotenv_path=env_path)

# ===============================================
# Database Connection Utility
# ===============================================

def get_db_connection():
    """
    Establishes and returns a PostgreSQL database connection using environment variables.

    Returns:
        connection (psycopg2.connection): Active database connection object.

    Raises:
        psycopg2.Error: If connection fails due to incorrect credentials or server issues.
    """
    try:
        connection = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        return connection
    except psycopg2.Error as e:
        print(f"❌ Database connection failed: {e}")
        raise
