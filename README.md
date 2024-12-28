# Social Engineering Game

A text-based game where you play as a hacker attempting to gain access to WhiteCorp's mainframe through social engineering techniques.

## Setup

1. Create a `.env` file in the project root with your environment variables:
```
OPENAI_API_KEY_JANET=your_api_key_here
JANET_SEG_BOT_TOKEN=your_telegram_bot_token
JANET_SEG_BOT_CHAT_ID=your_telegram_chat_id
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Run the game:
```bash
python game.py
```

To run the server with a custom port:
```bash
python server.py --port 8080
```

To run with Docker Compose:
```bash
# Development
docker compose up

# CI/Testing
docker compose -f docker-compose.ci.yml up
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

## Note

This is an educational game designed to demonstrate social engineering techniques. Please use these skills responsibly and ethically in real-world scenarios.

## Testing e2e locally

Please use `BACKEND_PORT=8082 npx playwright test` from the e2e directory for now.

## Things to do

[ ] Add CAPTCHA to the game
[ ] Add more background story
[ ] Display progress (which is really the intel you have gathered)
[ ] In the rules explain that each level is 0-shot