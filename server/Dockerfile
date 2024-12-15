FROM python:3.11-slim

ARG VERSION
ENV APP_VERSION=$VERSION

WORKDIR /app

# Install dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

ENV FLASK_ENV=production
ENV PORT=23925

LABEL org.opencontainers.image.version=${VERSION}

EXPOSE 23925

CMD ["python", "server.py"]
