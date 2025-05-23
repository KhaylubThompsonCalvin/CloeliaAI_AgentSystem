# =============================================================================
# File: main.py
# Project: CloeliaAI_AgentSystem
# Author: Khaylub Thompson-Calvin
# Date: 2025-05-10
#
# Purpose:
#   Bootstraps the FastAPI application, loads environment variables,
#   and registers symbolic perception routes for:
#     • Metatron Firewall Middleware
#     • /cloelia Emotion API
#     • /emotion Logging
#     • /trigger Symbolic Feed
#     • /firewall-log Event Review
#     • /gpt Symbolic GPT Interaction (Fully FastAPI Integrated)
#     • /gpt/test Jinja2 UI for Manual Testing
#
# Run:
#   uvicorn main:app --reload
# =============================================================================

from src.controllers.firewall_log_controller import firewall_log
from src.controllers.trigger_feed_controller import trigger_feed
from src.controllers.emotion_log_controller import emotion_log
from src.agents.cloelia_ai.cloelia_api import cloelia_router
from src.controllers.gpt_controller import gpt_router
from src.middleware.proxy_mind import ProxyMindMiddleware
import os
import traceback
from fastapi import FastAPI, Request, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from src.utils.config import get_db_connection


# Step 1: Load environment variables from .env
load_dotenv()

# Step 2: Initialize FastAPI app instance with metadata
app = FastAPI(
    title="Cloelia AI Agent System",
    description="Symbolic Emotional Insight API + GPT-4o-mini + ElevenLabs Audio Synthesis",
    version="0.1.0")

# Step 3: Mount Static Assets (CSS/JS/Audio Files)
app.mount(
    "/static",
    StaticFiles(directory=os.path.join("views", "static")),
    name="static"
)

app.mount(
    "/gpt/audio",
    StaticFiles(directory=os.path.join("static", "audio", "responses")),
    name="gpt_audio"
)


# Step 4: Configure Jinja2 Templates for UI Rendering
templates = Jinja2Templates(directory=os.path.join("views", "templates"))

# Step 5: Add Metatron-Inspired Firewall Middleware
app.add_middleware(ProxyMindMiddleware)

# -----------------------------------------------------------------------------
# Root Health Check (Hidden from OpenAPI Docs)
# -----------------------------------------------------------------------------


@app.get("/", include_in_schema=False)
def root():
    """
    Health check route for monitoring and deployment platforms.
    """
    return {"message": "Cloelia AI Agent System is online and operational."}

# -----------------------------------------------------------------------------
# GPT Symbolic Test UI (Jinja2)
# -----------------------------------------------------------------------------


@app.get("/gpt/test", tags=["GPT Interface"])
def gpt_test_ui(request: Request):
    """
    Renders the symbolic GPT test interface for manual message evaluation.
    """
    try:
        return templates.TemplateResponse(
            "gpt_test_ui.html",
            {"request": request}
        )
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={
                "error": "Template rendering failed",
                "details": str(e)
            }
        )


# -----------------------------------------------------------------------------
# GPT Symbolic API (FastAPI Router)
# -----------------------------------------------------------------------------

app.include_router(gpt_router, prefix="/gpt", tags=["GPT Symbolic API"])


@gpt_router.post("/generate-response")
async def generate_gpt_response(request: Request):
    """
    FastAPI route to handle GPT symbolic message processing.
    Calls Node.js GPT bridge and ElevenLabs audio synthesis.
    """
    return await gpt_controller.generate_response(request)


@gpt_router.get("/audio/{filename}")
async def serve_audio_file(filename: str):
    """
    Serve generated ElevenLabs audio responses.
    """
    return await gpt_controller.serve_audio(filename)


@app.get("/db/test", tags=["System Check"])
def db_test():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()
        conn.close()
        return {"status": "connected", "result": result}
    except Exception as e:
        return {"status": "error", "details": str(e)}


# Register GPT Router
app.include_router(gpt_router)

# -----------------------------------------------------------------------------
# Register All Other Routers (Modular Controllers)
# -----------------------------------------------------------------------------
app.include_router(cloelia_router, prefix="/cloelia", tags=["Cloelia"])

app.include_router(emotion_log, prefix="/emotion", tags=["Emotion Log"])

app.include_router(trigger_feed, prefix="/trigger", tags=["Symbolic Feed"])

app.include_router(firewall_log, prefix="/firewall-log", tags=["Firewall Log"])
