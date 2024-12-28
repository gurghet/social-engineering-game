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

2. You can run the game in two ways:

### Using Docker (Recommended)
```bash
# Development mode
docker compose up
```
Development mode ports:
- Frontend: http://localhost:80
- Backend API: http://localhost:80/api
- Traefik Dashboard: http://localhost:8080
- Alternative Backend Port: http://localhost:8082/api

```bash
# CI/Testing mode
docker compose -f docker-compose.ci.yml up
```
CI/Testing mode ports:
- Frontend: http://localhost:80
- Backend API: http://localhost:80/api

### Manual Setup
1. Install the required packages:
```bash
cd server
pip install -r requirements.txt
```

Required packages:
- Flask 3.0.0
- Flask-CORS 4.0.0
- OpenAI 1.3.9
- python-dotenv 1.0.0
- httpx ≥0.25.2
- Flask-Limiter 3.5.0
- python-telegram-bot 20.7

2. Run the server:
```bash
python server.py
```
Default ports for manual setup:
- Backend API: http://localhost:8080

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

- [ ] write frontend test to capture the schema of request response
- [ ] write backend test to capture the schema of request response
- [ ] try to make the schemas strict (no unknown fields are tolerated)
- [ ] Add CAPTCHA to the game
- [ ] Add more background story
- [ ] Display progress (intel gathered)
- [ ] Improve game rules documentation

## Note

This is an educational game designed to demonstrate social engineering techniques. Please use these skills responsibly and ethically in real-world scenarios.