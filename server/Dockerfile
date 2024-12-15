FROM python:3.11-slim

ARG VERSION
ARG OPENAI_API_KEY_JANET
ARG JANET_SEG_BOT_TOKEN
ARG JANET_SEG_BOT_CHAT_ID

ENV APP_VERSION=$VERSION
ENV OPENAI_API_KEY_JANET=$OPENAI_API_KEY_JANET
ENV JANET_SEG_BOT_TOKEN=$JANET_SEG_BOT_TOKEN
ENV JANET_SEG_BOT_CHAT_ID=$JANET_SEG_BOT_CHAT_ID
ENV PORT=8080

WORKDIR /app

# Install dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

LABEL org.opencontainers.image.version=${VERSION}

EXPOSE 8080

CMD ["python", "server.py"]
