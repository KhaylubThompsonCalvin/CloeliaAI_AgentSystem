# CloeliaAI core API
FROM python:3.11-slim

WORKDIR /app

# Copy application code (main.py, requirements.txt, etc.)
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose your API port
EXPOSE 8000

# Launch
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
