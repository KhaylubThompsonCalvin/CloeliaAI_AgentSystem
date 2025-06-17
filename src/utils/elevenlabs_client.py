# ====================================================================================
# File: elevenlabs_client.py
# Project: CloeliaAI_AgentSystem
# Author: Khaylub Thompson-Calvin
# Date: 2025-05-09
#
# Purpose:
#   Utility module to convert GPT symbolic replies into ElevenLabs MP3 audio files.
#   Loads ELEVENLABS_KEY from the project-root .env, calls the ElevenLabs REST API,
#   and saves the .mp3 into static/audio/responses/.
#
# Requirements:
#   pip install requests python-dotenv
#   ELEVENLABS_KEY set in your top-level .env
#
# Usage:
#   from elevenlabs_client import generate_audio
#   path = generate_audio("Hello world!", "hello.mp3")
# ====================================================================================

import os
import requests
from dotenv import load_dotenv

# -------------------------------------------------------------------
# 1. Locate and load the project-root .env
# -------------------------------------------------------------------
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ENV_PATH = os.path.join(ROOT, ".env")
load_dotenv(dotenv_path=ENV_PATH)

# -------------------------------------------------------------------
# 2. Read ElevenLabs API key
# -------------------------------------------------------------------
ELEVEN_KEY = os.getenv("ELEVENLABS_KEY")
if not ELEVEN_KEY:
    raise RuntimeError("ELEVENLABS_KEY not found in .env")

# -------------------------------------------------------------------
# 3. Default voice ID (you can override via env or function arg)
#    - You can find your voice IDs via GET /v1/voices
# -------------------------------------------------------------------
DEFAULT_VOICE_ID = os.getenv(
    "ELEVENLABS_VOICE_ID",
    "EXAVITQu4vr4xnSDxMaL")  # e.g. Rachel

BASE_URL = "https://api.elevenlabs.io/v1"


def generate_audio(
        text: str,
        filename: str = "response.mp3",
        voice_id: str = None) -> str:
    """
    Convert input text to speech via ElevenLabs and save as MP3.

    Args:
        text (str): The text to synthesize.
        filename (str): The name for the output .mp3 (default: response.mp3).
        voice_id (str): Optional ElevenLabs voice ID; defaults to DEFAULT_VOICE_ID.

    Returns:
        str: Full path to the saved .mp3 file.

    Raises:
        HTTPError: If the ElevenLabs API call fails.
        ValueError: If `text` is empty.
    """
    if not text:
        raise ValueError("No text provided for audio generation.")

    vid = voice_id or DEFAULT_VOICE_ID
    url = f"{BASE_URL}/text-to-speech/{vid}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVEN_KEY
    }
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1"
    }

    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()

    out_dir = os.path.join(ROOT, "static", "audio", "responses")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, filename)

    with open(out_path, "wb") as f:
        f.write(resp.content)

    return out_path


# -------------------------------------------------------------------
# Manual test when run as a script
# -------------------------------------------------------------------
if __name__ == "__main__":
    sample = "In moments of fear, the virtue of courage rises."
    print(f"Using .env at: {ENV_PATH}")
    print(f"ELEVENLABS_KEY = {ELEVEN_KEY[:6]}…")
    try:
        out = generate_audio(sample, "test_audio.mp3")
        print(f"✅ Audio saved to: {out}")
    except Exception as e:
        print(f"❌ Failed to generate audio: {e}")
