FROM python:3.11-slim

ARG VERSION
ENV APP_VERSION=$VERSION

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=server.py
ENV FLASK_ENV=production
ENV PORT=23925

LABEL org.opencontainers.image.version=${VERSION}

EXPOSE 23925

CMD ["python", "server.py"]
