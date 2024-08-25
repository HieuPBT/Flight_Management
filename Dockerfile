# Stage 1: Build Stage
FROM python:3.10-alpine AS builder

WORKDIR /app
COPY requirements.txt .
RUN apk add --no-cache gcc musl-dev libffi-dev && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt && \
    apk del gcc musl-dev libffi-dev

# Stage 2: Final Stage
FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=builder /install /usr/local

COPY . .

EXPOSE 5020

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5020", "flightapp.index:app"]