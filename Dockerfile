# Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY todo_app.py .
COPY test_todo.py .

CMD ["python", "todo_app.py"]