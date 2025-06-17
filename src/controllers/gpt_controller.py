# =============================================================================
# File: src/controllers/gpt_controller.py
# Project: CloeliaAI_AgentSystem
# Author: Khaylub Thompson-Calvin
# Date: 2025-05-10
#
# Purpose:
#   Provides FastAPI-based GPT interaction endpoints:
#     1. Accepts symbolic message via POST JSON.
#     2. Calls Node.js GPT bridge for a symbolic response.
#     3. Generates narrated audio via ElevenLabs.
#     4. Returns both GPT response and audio URL in JSON format.
#
# Dependencies:
#   - FastAPI for API Routing
#   - Node.js (gpt_bridge.mjs) for GPT integration
#   - ElevenLabs API via generate_audio()
#   - Audio files saved under static/audio/responses/
# =============================================================================

import subprocess
import json
import uuid
import os
import traceback
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from src.utils.elevenlabs_client import generate_audio

# Initialize FastAPI Router
gpt_router = APIRouter()

@gpt_router.get("/audio/{filename}")
async def serve_audio(filename: str):
    """
    Serve generated MP3 audio files for playback.

    Args:
        filename (str): The name of the audio file to serve.

    Returns:
        FileResponse: MP3 audio file for playback or download.
    """
    audio_dir = os.path.abspath(os.path.join("views", "static", "audio", "responses"))
    audio_path = os.path.join(audio_dir, filename)

    if not os.path.exists(audio_path):
        raise HTTPException(status_code=404, detail="Audio file not found.")

    return FileResponse(audio_path, media_type="audio/mpeg")

@gpt_router.post("/gpt/generate-response")
async def generate_response(request: Request):
    """
    Handle GPT symbolic message processing and audio generation.

    Process:
        1. Accept JSON with a "message" field.
        2. Call Node.js GPT bridge for AI response.
        3. Generate narration audio via ElevenLabs.
        4. Return GPT response text and audio URL.

    Returns:
        JSONResponse: {
            "response": {
                "text": "...",
                "audio_url": "..."
            }
        }
    """
    # 1️⃣ Validate Input Payload
    try:
        payload = await request.json()
        user_msg = payload.get("message", "").strip()
        print(f"📨 Incoming Message: {user_msg}")

        if not user_msg:
            raise HTTPException(status_code=400, detail="Message field is required.")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Invalid JSON payload: {str(e)}")

    # 2️⃣ Call Node.js GPT Bridge for AI Response
    try:
        print("🚀 Launching Node.js GPT Bridge...")
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

        proc = subprocess.run(
            ["node", "node_clients/gpt_bridge.mjs", user_msg],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
            encoding="utf-8",
            cwd=root_dir
        )

        stdout_clean = proc.stdout.strip()
        print(f"📄 Raw Subprocess Output: {stdout_clean}")

        # Verify JSON Format and "content" Field Presence
        if not stdout_clean.startswith("{") or '"content"' not in stdout_clean:
            raise HTTPException(status_code=500, detail="Invalid JSON output from GPT bridge.")

        reply = json.loads(stdout_clean)
        gpt_text = reply.get("content", "").strip()

        if not gpt_text:
            raise ValueError("GPT response contained empty content.")

        print(f"🧠 GPT Text: {gpt_text}")

    except subprocess.CalledProcessError as e:
        stderr_output = e.stderr.strip() if e.stderr else "No stderr output."
        print(f"❌ Node.js Error: {stderr_output}")
        if "Missing environment variable" in stderr_output:
            raise HTTPException(
                status_code=500,
                detail=f"GPT Bridge Environment Configuration Error: {stderr_output}"
            )
        raise HTTPException(status_code=500, detail=f"Node.js GPT bridge failed: {stderr_output}")

    except json.JSONDecodeError as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to parse GPT output: {str(e)}")

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Unhandled GPT bridge error: {str(e)}")

    # 3️⃣ Generate ElevenLabs Audio
    audio_file = f"reply_{uuid.uuid4().hex[:8]}.mp3"
    try:
        print(f"🎤 Generating audio for: {audio_file}")
        generate_audio(gpt_text, audio_file)
        print(f"✅ Audio generated successfully: {audio_file}")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Audio generation failed: {str(e)}")

    # 4️⃣ Final Response Construction
    audio_url = f"/gpt/audio/{audio_file}"
    print(f"📦 Final Response: text length={len(gpt_text)}, audio_url={audio_url}")

    return JSONResponse(content={
        "response": {
            "text": gpt_text,
            "audio_url": audio_url
        }
    })

