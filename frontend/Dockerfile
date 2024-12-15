# Build stage
FROM node:18 as builder

ARG VERSION
ENV VITE_APP_VERSION=$VERSION

WORKDIR /app

# Install dependencies first (better caching)
COPY package*.json ./
RUN npm ci

# Copy source code
COPY . .

# Build the app
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

LABEL org.opencontainers.image.version=${VERSION}
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
