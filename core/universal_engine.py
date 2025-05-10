# ========================================================================================
# File: universal_engine.py
# Purpose: Symbolic detection engine that analyzes recent user emotion logs and determines
# if a symbolic action should trigger. Matches emotion → virtue, and logs the trigger.
# ========================================================================================

from datetime import datetime, timedelta

class UniversalEngine:
    def __init__(self, db_conn):
        self.conn = db_conn

    def detect_symbolic_trigger(self, user_id):
        """
        Analyze recent logs to determine if a symbolic trigger should occur.
        """
        with self.conn.cursor() as cur:
            # Step 1: Fetch latest 5 emotion logs
            cur.execute("""
                SELECT emotion FROM EmotionLog
                WHERE user_id = %s
                ORDER BY timestamp DESC
                LIMIT 5;
            """, (user_id,))
            rows = cur.fetchall()

            if not rows:
                return None

            emotions = [row[0] for row in rows]
            dominant = max(set(emotions), key=emotions.count)

            # Step 2: Find matching virtue
            cur.execute("""
                SELECT virtue_id, name FROM VirtueEntry
                WHERE emotion_link = %s;
            """, (dominant,))
            virtue = cur.fetchone()

            if not virtue:
                return None

            # Step 3: Log symbolic trigger
            cur.execute("""
                INSERT INTO SymbolicTrigger (user_id, symbol, emotion_match, action_type, narration_file)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING trigger_id;
            """, (
                user_id,
                virtue[1],
                dominant,
                'reflection_prompt',
                f"narration_{virtue[1].lower()}.mp3"
            ))
            trigger_id = cur.fetchone()[0]
            self.conn.commit()

            return {
                "trigger_id": trigger_id,
                "emotion": dominant,
                "virtue": virtue[1],
                "action": "reflection_prompt"
            }
