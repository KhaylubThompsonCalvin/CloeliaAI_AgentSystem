import os
from dotenv import load_dotenv

# Explicitly define the path to the .env file
env_path = os.path.join(os.getcwd(), ".env")
print(f"📂 Current Working Directory: {os.getcwd()}")
print(f"📄 Loading .env from: {env_path}")

# Load the environment variables from the specified .env file
load_dotenv(dotenv_path=env_path)

# Retrieve and print the ELEVENLABS_KEY
print("🔑 ELEVENLABS_KEY =", os.getenv("ELEVENLABS_KEY"))



