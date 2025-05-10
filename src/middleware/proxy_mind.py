# ========================================================================================
# File: proxy_mind.py
# Project: CloeliaAI_AgentSystem
# Author: Khaylub Thompson-Calvin
# Date: 2025-05-08
#
# Purpose:
# Middleware firewall for Cloelia. This layer intercepts all incoming requests to:
# - Track symbolic "heartbeat" patterns per IP
# - Detect rapid/excessive requests symbolically (rate limiting)
# - Log all activity to proxy_mind_log.json for reflection, training, or retaliation
#
# Summary:
# This module lays the foundation for a symbolic cybersecurity layer, inspired by
# Kevin Mitnick-style logic — defending through awareness, deception, and reflection.
#
# Middleware:
# - Integrate this with FastAPI in `main.py` via `add_middleware(ProxyMindMiddleware)`
# ========================================================================================

import os
import json
import time
from datetime import datetime
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

# ---------------------------------------------------------------------------
# Define path to log file: stores symbolic firewall detections
# ---------------------------------------------------------------------------
FIREWALL_LOG = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "logs", "proxy_mind_log.json")
)

# ---------------------------------------------------------------------------
# Internal rate-limiting tracker per IP
# ---------------------------------------------------------------------------
REQUEST_TIMES = {}  # { ip_address: [timestamps] }


class ProxyMindMiddleware(BaseHTTPMiddleware):
    """
    Cloelia’s symbolic firewall middleware. Intercepts requests, checks for
    excessive frequency (symbolic 'overstimulus'), logs them, and optionally
    returns rate-limit warnings with reflective responses.
    """

    async def dispatch(self, request: Request, call_next):
        ip = request.client.host
        path = request.url.path
        now = time.time()

        # Track current request timestamps per IP
        if ip not in REQUEST_TIMES:
            REQUEST_TIMES[ip] = []
        REQUEST_TIMES[ip].append(now)

        # Remove timestamps older than 60 seconds
        REQUEST_TIMES[ip] = [t for t in REQUEST_TIMES[ip] if now - t < 60]

        too_frequent = len(REQUEST_TIMES[ip]) > 10  # >10 requests/min is suspicious

        # Log every interaction (whether threat or not)
        self.log_event(ip, path, too_frequent)

        # If too many requests, respond symbolically (HTTP 429)
        if too_frequent:
            return JSONResponse(
                content={
                    "error": "Cloelia has sensed an unnatural rhythm. Delay your inquiry."
                },
                status_code=429
            )

        # Continue processing request
        response = await call_next(request)
        return response

    def log_event(self, ip: str, path: str, threat: bool):
        """
        Logs every intercepted request to symbolic firewall log.

        Args:
            ip (str): Requestor IP address
            path (str): Endpoint path
            threat (bool): Whether this request was flagged as excessive
        """
        os.makedirs(os.path.dirname(FIREWALL_LOG), exist_ok=True)

        # Load or create log
        if os.path.exists(FIREWALL_LOG):
            with open(FIREWALL_LOG, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []

        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "ip": ip,
            "path": path,
            "threat_detected": threat
        }

        data.append(entry)

        # Save updated log
        with open(FIREWALL_LOG, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
