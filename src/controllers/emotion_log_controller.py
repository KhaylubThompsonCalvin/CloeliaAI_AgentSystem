# Writes emotion entries to PostgreSQL (cloeila_dev)

# src/controllers/emotion_log_controller.py
from fastapi import APIRouter, Request
from pydantic import BaseModel
from database import get_connection

emotion_log = APIRouter()


class EmotionEntry(BaseModel):
    user_id: int
    emotion: str
    context_note: str = None
    microexpression_img: str = None


@emotion_log.post("/log-emotion")
def log_emotion(entry: EmotionEntry):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO EmotionLog (user_id, emotion, context_note, microexpression_img)
        VALUES (%s, %s, %s, %s);
    """, (entry.user_id, entry.emotion, entry.context_note, entry.microexpression_img))

    conn.commit()
    cur.close()
    conn.close()

    return {"message": "Emotion logged successfully."}
