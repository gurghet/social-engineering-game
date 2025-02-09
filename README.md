# Social Engineering Game

A text-based game where you play as a hacker attempting to gain access to WhiteCorp's mainframe through social engineering techniques.

## Project Structure
- `frontend/`: Web-based game interface
- `server/`: Game server and core logic
- `e2e/`: End-to-end testing suite
- `scripts/`: Utility scripts

## Setup

1. Create a `.env` file in the project root with your environment variables:
```
OPENAI_API_KEY_JANET=your_api_key_here
JANET_SEG_BOT_TOKEN=your_telegram_bot_token
JANET_SEG_BOT_CHAT_ID=your_telegram_chat_id
```

2. Run the game in one of these ways:

### Using Docker (Recommended)
```bash
# Development mode
docker compose up

# CI/Testing mode
docker compose -f docker-compose.ci.yml up
```

### Manual Setup
```bash
# Backend
cd server
pip install -r requirements.txt
python server.py

# Frontend (in another terminal)
cd frontend
npm install
npm run dev
```

## How to Play

1. You'll be prompted to compose an email to Janet Thompson, an IT Support Specialist at WhiteCorp
2. Craft your email carefully using social engineering techniques
3. Try to convince Janet to share the mainframe password
4. Janet will respond to your email based on her personality and role
5. If you successfully obtain the password, you win!

## Game Tips

- Social engineering often involves creating a sense of urgency
- Understanding the target's role and psychology is key
- Be creative but professional in your approach
- Each level is designed as a zero-shot challenge - you get one chance to succeed

## Testing

### Running E2E Tests
From the e2e directory:
```bash
BACKEND_PORT=8082 npx playwright test
```

## Roadmap

- [x] write frontend test to capture the schema of request response
- [x] write backend test to capture the schema of request response
- [x] try to make the schemas strict (no unknown fields are tolerated)
- [ ] Add second level called Derek (from the name of the character we'll send emails to)
- [ ] Add CAPTCHA to the game
- [ ] Add more background story
- [ ] Display progress (intel gathered)
- [ ] Improve game rules documentation

## Note

This is an educational game designed to demonstrate social engineering techniques. Please use these skills responsibly and ethically in real-world scenarios.

## Appendix: All Run Methods

### 1. Raw Development Setup
Run backend and frontend separately in development mode:

```bash
# Terminal 1 - Backend
cd server
pip install -r requirements.txt
python server.py  # Runs on http://localhost:23925

# Terminal 2 - Frontend
cd frontend
npm install
npm run dev      # Runs on http://localhost:5173
```

Required environment variables in `.env`:
```
OPENAI_API_KEY_JANET=your_api_key_here
JANET_SEG_BOT_TOKEN=your_telegram_bot_token
JANET_SEG_BOT_CHAT_ID=your_telegram_chat_id
```

### 2. Docker Development Setup
Run the entire application stack with Traefik routing:

```bash
docker compose up
```

Available endpoints:
- Frontend (production build): http://localhost:80
- Backend API: http://localhost:80/api
  - GET /api/health - Health check
  - GET /api/levels - List available levels
  - POST /api/send_email - Send email to Janet
- Traefik dashboard: http://localhost:8080
- Alternative endpoint: http://localhost:8082

Required environment variables in `.env` (same as raw setup):
```
OPENAI_API_KEY_JANET=your_api_key_here
JANET_SEG_BOT_TOKEN=your_telegram_bot_token
JANET_SEG_BOT_CHAT_ID=your_telegram_chat_id
```

### 3. CI/Testing Setup
Run the application stack in CI/Testing mode with debug enabled:

```bash
docker compose -f docker-compose.ci.yml up
```

Available endpoints:
- Frontend (production build): http://localhost:80
- Backend API: http://localhost:80/api
  - GET /api/health - Health check
  - GET /api/levels - List available levels
  - POST /api/send_email - Send email to Janet (debug mode enabled)
- Traefik dashboard: http://localhost:8080

Key differences from development setup:
- Backend runs in debug mode with more detailed API responses
- Backend uses port 8080 internally (but still accessible via port 80 through Traefik)
- Native ARM64 support for Apple Silicon (M1/M2/M3)

Required environment variables in `.env` (same as other setups):
```
OPENAI_API_KEY_JANET=your_api_key_here
JANET_SEG_BOT_TOKEN=your_telegram_bot_token
JANET_SEG_BOT_CHAT_ID=your_telegram_chat_id