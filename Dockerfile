FROM python:3.12-slim

WORKDIR /app

# Install backend dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install frontend dependencies
COPY requirements-frontend.txt .
RUN pip install --no-cache-dir -r requirements-frontend.txt

# Copy application code
COPY backend/ backend/
COPY frontend/ frontend/
COPY app.py .

# Environment
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

# Expose ports
EXPOSE 5000 8000

# Start application
CMD ["python", "app.py"]
