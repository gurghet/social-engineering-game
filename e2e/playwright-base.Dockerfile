FROM mcr.microsoft.com/playwright:v1.40.0-focal

# Install only Chromium to keep the image size smaller
RUN npx playwright install --with-deps chromium
