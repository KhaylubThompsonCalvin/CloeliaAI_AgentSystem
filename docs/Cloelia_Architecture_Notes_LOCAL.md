# 🧠 Cloelia AI Agent System – Architecture & Developer Memory Log (LOCAL)

**Project Path:** `E:\CloudData\Desktop\Projects\Web Development\CloeliaAI_AgentSystem`
**File Purpose:** Personal system notes – not pushed to GitHub
**Created by:** Khaylub Thompson-Calvin
**Last Updated:** 2025-05-07

# Connect to PostgreSQL directly

cd "E:\Tools\PostgreSQL\17\bin"
.\psql -U postgres -p 8888

# Create or view database content

CREATE DATABASE cloeila_dev;
\c cloeila_dev
SELECT \* FROM UserProfile;

# Seed table (future):

python seed_virtues.py

---

## ✅ 1. Project Overview

Cloelia is a symbolic emotional AI system that:

- Accepts emotional input from users
- Detects symbolic meaning or virtue triggers
- Returns responses tied to behavior, wisdom, or training
- Logs activity in a PostgreSQL database
- Integrates with OpenAI + ElevenLabs in later phases
- Is part of the larger EyesUnclouded Universe and legacy training system

---

## ⚙️ 2. Startup Checklist

To run the app locally:

```bash
# 1. Activate the virtual environment
.\venv\Scripts\activate

# 2. Start the FastAPI app with hot reload
uvicorn main:app --reload

# 3. Open browser to:
http://127.0.0.1:8000



 3. File/Folder Key Map
Path	Purpose
main.py	Starts FastAPI and includes routers
src/agents/cloelia_ai/cloelia_api.py	Handles /analyze-emotion
src/core/universal_algorithm.py	Symbolic pattern engine
src/core/symbolic_graph.py	Metatron Cube (virtue/emotion mapping)
database.py	Connects to PostgreSQL using .env
docs/test_cloelia_api_cases.md	Manual test case log
tests/test_cloelia_api.py	API call test script using requests
static/images/expressions/	Facial images for training/game
.env	Stores all API keys and DB config
render.yaml	Deployment config (Render)

🧬 4. Database Memory (PostgreSQL)
DB Name:
nginx
Copy
Edit
cloeila_dev
Tables You’ve Created:
UserProfile

EmotionLog

PerceptionLog

VirtueEntry

SymbolicTrigger

AudioNarration

OracleArchiveEntry

MentorInsight

CloeliaTask

How It Works:
Emotions are sent via API → logged

Patterns are detected in universal_algorithm.py

Matches are returned from VirtueEntry and SymbolicTrigger

Future expansion includes streak logic, reflection tracking, and AI narration

🎮 5. Emotion Picture Game System (Skeleton Confirmed)
Already created:

swift
Copy
Edit
static/images/expressions/
├── anger/
├── happiness/
├── sadness/
├── surprise/
├── fear/
├── contempt/
├── disgust/
├── neutral/
🧠 Future Game Plan:

Show user random expression image

Let them guess emotion (CLI or Web)

Compare to folder label (truth)

Log result to EmotionLog

Analyze pattern via PerceptionLog

Raise perception_score or unlock insights

Optional Enhancements:

ElevenLabs audio feedback (“Correct. That was fear.”)

Role-specific UI hints (Seeker vs Strategist)

OpenAI explanation if user is wrong

Game unlocks or dashboard streaks


. To-Do (Coming Soon)
 Create /log-emotion route and controller

 Implement seed_virtues.py to insert core virtues

 Add /mentor-insight route (based on RoleType)

 Add /oracle-analyze route (OpenAI + ElevenLabs)

 Connect ElevenLabs audio per Role

 Track longest streaks via PerceptionLog

 Build frontend “Emotion Game” (Flask or JS)

🧠 Final Notes
Cloelia is the foundation for symbolic perception training.
This system is part of your broader legacy architecture in EyesUnclouded.

It trains users (or descendants) to:

Read emotional patterns

Make wise decisions

Navigate virtue through conflict

And prepares them to one day inherit symbolic insight + value.

"To see the world with eyes unclouded."
```

📂 Inside src/
Folder Purpose
agents/ Contains Cloelia’s route logic and symbolic response logic
controllers/ For expanding Flask-style modular routes (auth, emotion logging)
core/ Universal algorithm, symbolic graph engine (Metatron cube logic)
models/ SQL models if you add SQLAlchemy later (currently manual SQL)
utils/ Helper scripts, seeders (e.g., seed_virtues.py, audio tools)
