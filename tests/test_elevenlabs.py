# =============================================================================
# File: tests/test_elevenlabs.py
# Purpose: Directly tests ElevenLabs API integration.
# =============================================================================

import sys
import os

# Ensure the project root is in sys.path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils.elevenlabs_client import generate_audio

if __name__ == "__main__":
    try:
        test_text = "This is a test of the Eleven Labs voice API."
        audio_filename = "elevenlabs_test.mp3"
        generate_audio(test_text, audio_filename)
        print(f"✅ Audio generated: {audio_filename}")
    except Exception as e:
        print(f"❌ Error generating audio: {e}")

