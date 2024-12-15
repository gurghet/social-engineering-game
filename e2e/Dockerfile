FROM mcr.microsoft.com/playwright:v1.40.0-focal

WORKDIR /e2e

# Copy package files first to leverage Docker cache
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy test files
COPY tests ./tests
COPY playwright.config.ts ./

# Install Playwright browsers with dependencies
RUN npx playwright install --with-deps chromium

# Keep container running for docker-compose
CMD ["tail", "-f", "/dev/null"]
