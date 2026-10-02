FROM python:3.10-slim
RUN useradd -u 1000 appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser . .

USER appuser

CMD ["python", "41_scan_stream_default.py"]
