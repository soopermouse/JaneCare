FROM python:3.12-slim
WORKDIR /app
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt
COPY . /app
EXPOSE 8090
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8090"]
