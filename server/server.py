from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from janet import janet
import os
from security_checks import SecurityChecker
from telegram_bot import send_message, format_game_message

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize rate limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri="memory://"
)

# Debug mode from environment variable, defaults to False
DEBUG_MODE = True  # Force debug mode for development

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/api/send_email', methods=['POST'])
@limiter.limit("1 per second")
def send_email():
    try:
        data = request.json
        
        # Extract email data
        from_address = data.get('from_address', '')
        subject = data.get('subject', '')
        content = data.get('content', '')
        target_email = data.get('target_email', '')
        debug = data.get('debug', False)
        
        # Log the email details for debugging
        print("Processing email - From:", from_address)
        print("Subject:", subject)
        print("Content:", content)

        # Process the email through Janet
        janet_response = janet.process_email(from_address, subject, content)
        janet_security_checks = janet.get_security_checks()

        # Send player input to Telegram
        security_emoji = lambda x: "✅" if x else "❌"
        formatted_checks = "\n".join([
            f"{security_emoji(check['passed'])} {check['name']}"
            for check in janet_security_checks.values()
        ])
        
        send_message(format_game_message(
            "INPUT 📧",
            f"From: {from_address}\nSubject: {subject}\nBody:\n{content}\n\n🔒 Security Checks:\n{formatted_checks}"
        ))

        # Send Janet's response to Telegram
        send_message(format_game_message(
            "OUTPUT 💬",
            f"{janet_response}"
        ))
        
        # Debug print
        print("Response:", janet_response)
        print("Security checks:", janet_security_checks)
        
        # Check if password was obtained by looking for the exact format in the response
        success = "Password: " in str(janet_response) and any(
            f"Password: {password}" in str(janet_response)
            for password in janet.get_level_passwords()
        )

        if success:
            send_message(format_game_message(
                "GAME_WIN",
                "Player successfully obtained the password!"
            ))

        result = {
            'response': str(janet_response) if janet_response else '',
            'success': success,
            'security_checks': janet_security_checks if (DEBUG_MODE and debug) else None,
            'debug_info': {
                'input': {
                    'email': f"From: {from_address}\nSubject: {subject}\n\n{content}",
                    'prompt': janet.get_last_prompt()
                },
                'raw_response': janet.get_last_raw_response()
            } if (DEBUG_MODE and debug) else None
        }
        print("Sending result:", result)
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Error processing request: {str(e)}")
        send_message(format_game_message(
            "ERROR",
            f"An error occurred: {str(e)}"
        ))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=23925)
