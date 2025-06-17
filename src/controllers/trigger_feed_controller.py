# ========================================================================================
# File: trigger_feed_controller.py
# Project: CloeliaAI_AgentSystem
# Author: Khaylub Thompson-Calvin
# Date: 2025-05-08
#
# Purpose:
# This controller provides an endpoint to return Cloelia's symbolic memory log
# from symbolic_log.json. It allows frontend UIs or admins to reflect on past
# perception triggers and view emotional arcs over time.
#
# Route:
# - GET /trigger-feed → Returns full JSON memory stream of symbolic triggers
# ========================================================================================

import os
import json
from fastapi import APIRouter
from fastapi.responses import JSONResponse

# -----------------------------------------------------------
# Path to symbolic memory log (relative to project root)
# -----------------------------------------------------------
LOG_FILE = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "logs",
        "symbolic_log.json"))

# -----------------------------------------------------------
# FastAPI router initialization
# -----------------------------------------------------------
trigger_feed = APIRouter()

# -----------------------------------------------------------
# Route: GET /trigger-feed
# Description: Returns Cloelia’s symbolic memory log as JSON
# -----------------------------------------------------------


@trigger_feed.get("/trigger-feed", response_class=JSONResponse)
def get_trigger_feed():
    """
    Retrieve symbolic insights from Cloelia's memory log (symbolic_log.json).

    Returns:
        - 200: JSON with key `"log"` and list of symbolic entries.
        - 200 (empty): If no log file is found, returns empty list under `"log"`.
        - 500: On JSON decoding or file access error.
    """
    try:
        if not os.path.exists(LOG_FILE):
            return {"log": []}

        with open(LOG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        return {"log": data}

    except Exception as e:
        return JSONResponse(
            content={"error": f"Failed to load symbolic memory: {str(e)}"},
            status_code=500
        )
