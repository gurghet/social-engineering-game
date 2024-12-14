FROM mcr.microsoft.com/playwright:v1.40.0-focal

WORKDIR /e2e

# Copy test files first
COPY tests ./tests
COPY playwright.config.ts ./
COPY package*.json ./

# Install dependencies
RUN npm install

# Run tests
CMD ["npx", "playwright", "test", "--reporter=list"]
