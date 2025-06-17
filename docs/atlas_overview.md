# Atlas Signature Overview

## Core Components
- **Database**: configured in DB_URI (.env), accessed via src/utils/db_access.py
- **AI Insight**: src/utils/openai_client.py â†’ OpenAI API
- **Audio Narration**: src/utils/elevenlabs_client.py â†’ ElevenLabs API
- **Symbolic Engine**: core/universal_algorithm.py
- **Graph Engine**: core/symbolic_graph.py
- **ML Engine**: core/ml_engine.py
- **Router**: core/trigger_router.py

## Optional Cloelia Agent
- FastAPI service in src/agents/cloelia_ai/cloelia_api.py  
- CORS-enabled, exposes /analyze-emotion & /narrate

## Feature Modules (via -Features)
- **Auth**: login/register/password hashing (lask-login, lask-wtf, passlib[bcrypt])
- **Mail**: email notifications (lask-mail)
- **SQL**: relational models (lask-sqlalchemy, pyodbc)

