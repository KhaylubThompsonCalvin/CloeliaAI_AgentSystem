# ========================================================================================
# File: database.py
# Purpose: PostgreSQL connection helper for the CloeliaAI Agent System
# Note: Uses psycopg2 + dotenv for secure configuration
# ========================================================================================

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME", "cloeila_dev"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "8888")
    )
