FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    TRAVEL_PLANNER_PORT=8765

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt \
    && python -m playwright install --with-deps chromium

COPY travel_planner_cli.py /app/travel_planner_cli.py
COPY travel_planner_server.py /app/travel_planner_server.py
COPY frontend /app/frontend
COPY README.md /app/README.md

EXPOSE 8765

CMD ["uvicorn", "--app-dir", "/app", "travel_planner_server:app", "--host", "0.0.0.0", "--port", "8765"]
