# ========================================================================================
# File: cloelia_proxy_behavior.py
# Project: CloeliaAI_AgentSystem
# Author: Khaylub Thompson-Calvin
# Date: 2025-05-09
#
# Purpose:
# mitmproxy addon that listens to incoming HTTP requests and checks for custom symbolic
# headers such as 'X-Symbolic-Emotion' and 'X-User-ID'. If detected, it sends this data
# to the /cloelia/analyze-emotion API and logs the symbolic feedback locally.
#
# Output:
# - Logs symbolic results to 'proxy_symbolic_emotion_log.json'
#
# Usage:
# Run mitmproxy with:
#   mitmproxy -s src/mitm_addons/cloelia_proxy_behavior.py
# ========================================================================================

import os
import json
import requests
from datetime import datetime
from mitmproxy import http

# Path to store symbolic proxy logs
LOG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs", "proxy_symbolic_emotion_log.json"))

def log_result(entry):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)

    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def request(flow: http.HTTPFlow) -> None:
    """
    Called when a client request is received. If symbolic headers exist,
    forward them to the Cloelia emotion engine and log the symbolic feedback.
    """
    headers = flow.request.headers

    if "X-Symbolic-Emotion" in headers and "X-User-ID" in headers:
        try:
            payload = {
                "user_id": int(headers["X-User-ID"]),
                "emotion": headers["X-Symbolic-Emotion"]
            }

            response = requests.post("http://127.0.0.1:8000/cloelia/analyze-emotion", json=payload)
            symbolic_result = response.json()

            log_entry = {
                "timestamp": datetime.utcnow().isoformat(),
                "ip": flow.client_conn.address[0],
                "emotion": payload["emotion"],
                "user_id": payload["user_id"],
                "symbolic_response": symbolic_result
            }

            log_result(log_entry)

        except Exception as e:
            log_result({
                "timestamp": datetime.utcnow().isoformat(),
                "error": str(e)
            })
