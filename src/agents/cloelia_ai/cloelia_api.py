# ========================================================================================
# File: cloelia_api.py
# Project: CloeliaAI_AgentSystem
# Author: Khaylub Thompson-Calvin
# Date: 2025-05-08
#
# Purpose:
# FastAPI router module for Cloelia's emotional insight engine. This endpoint receives
# structured emotion input and invokes the UniversalEngine to detect symbolic patterns
# from recent emotion logs. If a pattern matches, it returns a virtue, action, and trigger ID.
#
# Description:
# This module follows modular N-tier architecture, combining API routing (Controller Layer)
# with logic abstraction (Engine Layer) and database connectivity (Database Layer).
# It also logs symbolic events to a persistent symbolic memory file.
#
# Routes:
# - GET    /cloelia/              → Router health check
# - POST   /cloelia/analyze-emotion → Analyze recent logs to trigger symbolic insight
# ========================================================================================

from fastapi import APIRouter
from pydantic import BaseModel
from core.universal_engine import UniversalEngine            # Symbolic logic engine
from database import get_connection                          # DB connection helper
from src.utils.logger import log_symbolic_trigger                # Log symbolic insight to JSON

# -----------------------------------------------------------
# Initialize FastAPI router for Cloelia endpoint group
# -----------------------------------------------------------
cloelia_router = APIRouter()

# -----------------------------------------------------------
# Data model for incoming emotion analysis requests
# -----------------------------------------------------------
class EmotionRequest(BaseModel):
    """
    Represents a request to analyze symbolic emotional patterns for a given user.

    Fields:
    - user_id: int → The ID of the user in the UserProfile table
    - emotion: str → The latest reported emotion (e.g., 'anger')
    """
    user_id: int
    emotion: str

# -----------------------------------------------------------
# Route: GET /cloelia/
# Description: Health check route for CI/CD and diagnostics
# -----------------------------------------------------------
@cloelia_router.api_route("/", methods=["GET", "HEAD"])
def read_status():
    """
    Returns a status response indicating the Cloelia router is online.
    """
    return {"status": "Cloelia AI router is online."}

# -----------------------------------------------------------
# Route: POST /cloelia/analyze-emotion
# Description: Analyze recent emotion logs for symbolic triggers
# -----------------------------------------------------------
@cloelia_router.post("/analyze-emotion")
async def analyze_emotion(req: EmotionRequest):
    """
    Accepts user emotion input and analyzes recent emotional patterns to determine
    if a symbolic trigger (e.g., virtue reflection, legacy unlock) should activate.

    Process:
    1. Connects to the PostgreSQL database
    2. Uses UniversalEngine to scan recent logs
    3. Matches dominant emotion to a virtue (from VirtueEntry)
    4. Inserts a symbolic trigger into SymbolicTrigger table
    5. Logs the result to symbolic_log.json

    Returns:
    - emotion_detected: Dominant emotion
    - suggested_virtue: Mapped virtue response
    - action: Recommended symbolic action (e.g., 'reflection_prompt')
    - trigger_id: Database ID of the symbolic trigger

    Errors:
    - Returns a descriptive error message on failure
    """
    try:
        # Step 1: Connect to database
        conn = get_connection()

        # Step 2: Run symbolic detection engine
        engine = UniversalEngine(conn)
        result = engine.detect_symbolic_trigger(req.user_id)

        # Step 3: Close DB connection
        conn.close()

        # Step 4: Return result or no-match message
        if result:
            log_symbolic_trigger({
                "user_id": req.user_id,
                "emotion": result["emotion"],
                "virtue": result["virtue"],
                "action": result["action"],
                "trigger_id": result["trigger_id"]
            })

            return {
                "emotion_detected": result["emotion"],
                "suggested_virtue": result["virtue"],
                "action": result["action"],
                "trigger_id": result["trigger_id"]
            }
        else:
            return {"message": "No symbolic pattern detected."}

    except Exception as e:
        return {"error": f"Failed to analyze emotion: {str(e)}"}


