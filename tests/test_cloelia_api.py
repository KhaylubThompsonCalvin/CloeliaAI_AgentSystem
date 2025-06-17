# Cloelia Agent API Test Script
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("CLOELIA_API_KEY")
if not API_KEY:
    print("❌ CLOELIA_API_KEY not found in environment.")
    exit()

url = "https://cloeliaai.onrender.com/analyze-emotion"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}
payload = {"emotion": "focus"}

try:
    response = requests.post(url, headers=headers, json=payload)
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
except Exception as e:
    print("❌ Error during request:", str(e))
