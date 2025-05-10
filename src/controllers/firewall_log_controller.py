# ========================================================================================
# File: firewall_log_controller.py
# Project: CloeliaAI_AgentSystem
# Author: Khaylub Thompson-Calvin
# Date: 2025-05-08
#
# Purpose:
# Exposes a FastAPI route to retrieve Cloelia's symbolic firewall log, which records
# IP request behavior and detects rate-limit threats. This route serves as a
# visualization and analysis tool for symbolic defense patterns.
#
# Description:
# Returns the contents of proxy_mind_log.json. If no file exists yet, it returns
# an empty list. Used by devs or admins to review requests flagged by ProxyMind.
#
# Route:
# - GET /firewall-log → Returns a list of request logs with timestamps, IPs, and threat flags.
# ========================================================================================

from fastapi import APIRouter
from fastapi.responses import JSONResponse
import os
import json

# -----------------------------------------------------------------------------
# Define router instance to be included in main.py
# -----------------------------------------------------------------------------
firewall_log = APIRouter()

# -----------------------------------------------------------------------------
# Dynamically resolve the path to the firewall log file
# -----------------------------------------------------------------------------
LOG_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "logs", "proxy_mind_log.json")
)

# -----------------------------------------------------------------------------
# Route: GET /firewall-log
# Description: Returns contents of Cloelia's symbolic firewall memory log
# -----------------------------------------------------------------------------
@firewall_log.get("/firewall-log", response_class=JSONResponse)
def get_firewall_log():
    """
    Retrieve all symbolic firewall log entries.

    Returns:
        - 200 OK: JSON response with a list of request logs under "log" key.
        - 200 OK: Empty list if no log file exists yet.
        - 500 Internal Server Error: On read/parse failure.
    """
    try:
        # If no log file exists yet, return empty list
        if not os.path.exists(LOG_PATH):
            return JSONResponse(content={"log": []}, status_code=200)

        # Load and return log file contents
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        return JSONResponse(content={"log": data}, status_code=200)

    except Exception as e:
        # Return error if file read or JSON parsing fails
        return JSONResponse(
            content={"error": f"Unable to load firewall log: {str(e)}"},
            status_code=500
        )
