import os
from pathlib import Path
from dotenv import load_dotenv

# Finds the .env in the project root
env_path = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(dotenv_path=env_path)
