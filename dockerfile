FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p /app/data && useradd -u 10001 -m appuser && chown -R appuser /app
USER appuser
ENV PYTHONDONTWRITEBYTECODE=1
EXPOSE 8000
CMD ["uvicorn","server:app","--host","0.0.0.0","--port","8000","--workers","1"]
