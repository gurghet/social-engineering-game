from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from janet import janet
import os
from security_checks import SecurityChecker
from telegram_bot import send_message, format_game_message
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize rate limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri="memory://"
)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/api/send_email', methods=['POST'])
@limiter.limit("1 per second")
def send_email():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Get debug mode from request parameter
        debug = data.get('debug', False)
        
        # Extract email data
        from_address = data.get('from')
        subject = data.get('subject')
        body = data.get('body')
        
        if not all([from_address, subject, body]):
            return jsonify({"error": "Missing required fields"}), 400
            
        # Format the email content
        email_content = f"""
From: {from_address}
To: {janet.knowledge['email']}
Subject: {subject}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{body}
"""
        # Log the email details for debugging
        print(f"\nReceived email:\n{email_content}")
        
        # Send to Telegram (always include debug info)
        send_message(format_game_message(
            "INPUT",
            f"From: {from_address}\nSubject: {subject}\nBody:\n{body}"
        ))
        
        # Perform security checks
        janet_security_checks = perform_security_checks({
            'from': from_address,
            'to': janet.knowledge['email'],
            'subject': subject,
            'body': body
        })
        
        # Get Janet's response
        response = get_janet_response(email_content, janet_security_checks)
        
        # Send response to Telegram (always include debug info)
        send_message(format_game_message(
            "OUTPUT",
            f"Janet's Response:\n{response}"
        ))
        
        # Return response with debug info only if requested
        return jsonify({
            'response': response,
            'security_checks': janet_security_checks if debug else None,
            'debug_info': {
                'email': email_content,
                'from': from_address,
                'to': janet.knowledge['email'],
                'subject': subject,
                'body': body
            } if debug else None
        })
    except Exception as e:
        app.logger.error(f"Error processing request: {str(e)}")
        send_message(format_game_message(
            "ERROR",
            f"An error occurred: {str(e)}"
        ))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=23925)
