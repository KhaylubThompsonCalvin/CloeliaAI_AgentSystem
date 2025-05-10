# CloeliaAI Agent System – API Test Suite

# Branch: Emotional Insight Engine (Symbolic Trigger + Virtue Reflection + Proxy Firewall Integration)

# Name: Khaylub Thompson-Calvin

# Date: 2025-05-09

"""
This document contains complete test cases for the Cloelia Agent FastAPI system. It verifies:

- Emotion intake and symbolic trigger logic
- SQL + JSON logging systems
- Proxy-based emotional interception
- Firewall rate-limiting and defense behavior
- Foundation for future integrations (OpenAI, ElevenLabs, LangChain)
  """

---

## ✅ Test Case 1: Activate Virtual Environment

### Command:

```bash
.env\Scriptsctivate
```

---

## ✅ Test Case 2: Launch FastAPI Server

### Command:

```bash
uvicorn main:app --reload
```

**Expected Output**:

- Server running on http://127.0.0.1:8000
- “Application startup complete.”

---

## ✅ Test Case 3: Environment Variables (.env)

Ensure the following are defined:

- CLOELIA_API_KEY
- DB_PASSWORD
- OPENAI*KEY *(future)\_
- ELEVENLABS*KEY *(future)\_

---

## ✅ Test Case 4: Router Health Check

### Request:

```http
GET /cloelia/
```

**Expected Response**:

```json
{ "status": "Cloelia AI router is online." }
```

---

## ✅ Test Case 5: Emotion Analysis

### Request:

```http
POST /cloelia/analyze-emotion
```

### Body:

```json
{ "user_id": 1, "emotion": "anger" }
```

**Expected**: 200 OK, returns emotion_detected, virtue, action, trigger_id

---

## ✅ Test Case 6: Invalid Emotion Format

### Body:

```json
{ "user_id": 1, "emotion": 123 }
```

**Expected**: 422 Unprocessable Entity

---

## ✅ Test Case 7: Missing Emotion Field

```json
{ "user_id": 1 }
```

**Expected**: 422 Validation Error

---

## ✅ Test Case 8: No Symbolic Match

```json
{ "user_id": 99, "emotion": "unknown_emotion" }
```

**Expected**:

```json
{ "message": "No symbolic pattern detected." }
```

---

## ✅ Test Case 9: Symbolic Trigger Log Check

```powershell
Get-Content .\src\logs\symbolic_log.json
```

**Expected**: Entries include user_id, emotion, virtue, trigger_id

---

## ✅ Test Case 10: Proxy Middleware Activation

```bash
mitmproxy --mode regular@8082 -s src/mitm_addons/cloelia_proxy_behavior.py
```

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8000/cloelia/analyze-emotion" `
  -Method POST `
  -Body (@{ "user_id" = 1; "emotion" = "anger" } | ConvertTo-Json) `
  -ContentType "application/json" `
  -Headers @{ "X-User-ID" = "1"; "X-Symbolic-Emotion" = "anger" } `
  -Proxy "http://127.0.0.1:8082"
```

**Expected**: Symbolic response logged in `proxy_symbolic_emotion_log.json`

---

## ✅ Test Case 11: Firewall Rate Limiting

```powershell
for ($i=1; $i -le 12; $i++) {
  Invoke-RestMethod -Uri "http://127.0.0.1:8000/cloelia/" -Method GET
  Start-Sleep -Milliseconds 500
}
```

**Expected**: Final requests return 429 with symbolic warning

---

## ✅ Test Case 12: Inspect Firewall Log File

```powershell
Get-Content .\src\logs\proxy_mind_log.json
```

**Expected**: Look for `"threat_detected": true` entries

---

## ✅ Test Case 13: Inspect Proxy Symbolic Log File

```powershell
Get-Content .\src\logs\proxy_symbolic_emotion_log.json
```

**Expected**: Proxy entries with `emotion`, `user_id`, `symbolic_response`

---

## ✅ Test Case 14: Firewall Log API Route

```http
GET /firewall-log
```

**Expected**:

```json
{
  "log": [
    { "timestamp": "...", "ip": "...", "path": "...", "threat_detected": true }
  ]
}
```

---

# Test Case 15: OpenAI GPT Test via Node Client

# Goal: Verify OpenAI GPT API works via Node.js script using .env for secure key access.

# Setup:

# Node version 18+

# Packages installed: npm install openai dotenv

# File: node_clients/gpt_test.mjs

# .env contains valid OPENAI_KEY

# command to Run:

# bash

# Copy

# node node_clients/gpt_test.mjs

# Expected Output:

# ✅ GPT Response: {

# role: 'assistant',

# content: 'Lines of code entwined,\nSilent thoughts in circuits hum,\nDreams of mind and heart.',

...

# }

# Result Log Suggestion (Optional):

# Save successful replies to logs/gpt_test_log.json for future traceability and symbolic mapping.

## 🧪 System Module Integration Table

# Test Case 16: GPT + Audio API Integration Successful

# Test Objective

# Verify full symbolic message processing pipeline:

# Node.js GPT bridge returns a valid response.

# ElevenLabs successfully generates narration audio.

# Final API response includes both text and valid audio URL.

# Preconditions

# FastAPI server is running:

# uvicorn main:app --reload

# ode.js environment properly configured.

# .env file contains valid OPENAI_KEY and ELEVENLABS_KEY.

# Audio output directory: views/static/audio/responses/ exists.

# PowerShell Test Command

# Invoke-RestMethod `

# -Uri "http://127.0.0.1:8000/gpt/generate-response" `

# -Method POST `

# -ContentType "application/json" `

# -Body '{"message":"Hello, brave one"}'

# Expected Output

# {

# "response": {

# "text": "Hello! How can I assist you today?",

# "audio_url": "/gpt/audio/reply_d585848e.mp3"

# }

# }

# Backend Logs Verification

# 📨 Incoming Message: Hello, brave one

# 🚀 Launching Node.js GPT Bridge...

# 📄 Raw Subprocess Output: {"role":"assistant","content":"Hello! How can I assist you today?"}

# 🧠 GPT Text: Hello! How can I assist you today?

# 🎤 Generating audio for: reply_d585848e.mp3

# ✅ Audio generated successfully: reply_d585848e.mp3

# 📦 Final Response: text length=34, audio_url=/gpt/audio/reply_d585848e.mp3

| Module                            | Function                          | Status |
| --------------------------------- | --------------------------------- | ------ |
| `UniversalEngine`                 | Symbolic logic layer              | ✅     |
| `SymbolicTrigger`                 | Emotional pattern logs (SQL/JSON) | ✅     |
| `proxy_mind.py`                   | Rate-limit + deception layer      | ✅     |
| `cloelia_proxy_behavior.py`       | mitmproxy behavior for headers    | ✅     |
| `proxy_mind_log.json`             | Firewall log                      | ✅     |
| `proxy_symbolic_emotion_log.json` | Symbolic proxy reflection logs    | ✅     |
| `symbolic_log.json`               | Core symbolic insights            | ✅     |

---

## 🔄 Future Tests (Phase 3 Targets)

- [ ] /log-emotion (raw DB logging)
- [ ] /mentor-insight (lessons per Role)
- [ ] /oracle-analyze (LangChain + OpenAI summaries)
- [ ] ElevenLabs narration delivery
- [ ] Perception streak logic
- [ ] Class + Role unlock engine (gamified)
- [ ] Symbolic dashboard UI (HTML)

---

## 📁 Pytest Script

```bash
python tests/test_cloelia_api.py
```

---

## ✅ End of Test Plan – Phase 2 (Firewall + Proxy Complete)

## 🧪 System Modules Check

| Module                   | Function                   | Status               |
| ------------------------ | -------------------------- | -------------------- |
| `universal_algorithm.py` | Symbolic pattern detector  | ✅                   |
| `symbolic_graph.py`      | Metatron cube graph engine | ✅                   |
| `VirtueEntry` table      | Seeded with core virtues   | 🔜 (seed_virtues.py) |
| `SymbolicTrigger` table  | Logs emotional triggers    | ✅                   |
| `AudioNarration` table   | For future ElevenLabs ties | 🔜                   |
| `MentorInsight` table    | Role-specific lessons      | 🔜                   |
| `OracleArchiveEntry`     | Reflection log system      | 🔜                   |

---

## 🔄 Future Test Coverage (To Do)

- [ ] `/log-emotion` route (logs raw emotions to DB)
- [ ] `/mentor-insight` route (returns lessons per Role)
- [ ] `/oracle-analyze` (OpenAI + ElevenLabs summary)
- [ ] Emotion streak detection logic
- [ ] Audio file delivery with ElevenLabs response
- [ ] Legacy unlocking with class/role integration
- [ ] Dashboard recommendation response testing

---

## 📁 Test Script

File:

```bash
tests/test_cloelia_api.py
```

Command:

```bash
python tests/test_cloelia_api.py
```

---

## ✅ End of Test Plan – Phase 1
