FROM mcr.microsoft.com/playwright:v1.40.0-focal

WORKDIR /e2e

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy test files
COPY . .

# Run tests
CMD ["npx", "playwright", "test", "--reporter=list"]
