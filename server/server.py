from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from janet import janet
import os
from security_checks import SecurityChecker, perform_security_checks
from telegram_bot import send_message, format_game_message
from datetime import datetime
from game import get_janet_response
from levels import game_levels
import argparse

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure testing mode
app.config['TESTING'] = os.environ.get('FLASK_TESTING', 'False').lower() == 'true'

# Initialize rate limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri="memory://",
    default_limits=[],
    enabled=not app.config['TESTING']  # Disable rate limiting during tests
)

@app.errorhandler(429)  # HTTP 429 Too Many Requests
def ratelimit_handler(e):
    # Get the current limit that was exceeded
    limit = getattr(e, 'description', 'Rate limit exceeded')
    
    # Send notification via Telegram
    send_message(format_game_message(
        "RATE_LIMIT",
        f"Rate limit exceeded: {limit}\nIP: {get_remote_address()}"
    ))
    
    return jsonify({
        "error": "Too many requests",
        "description": limit
    }), 429

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/api/send_email', methods=['POST'])
@limiter.limit("1000 per day")
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
        
        # Perform security checks
        janet_security_checks = perform_security_checks({
            'from_address': from_address,
            'subject': subject,
            'body': body
        }, janet.knowledge['supervisor_email'])
        
        # Get Janet's response with the security checks
        response = get_janet_response(email_content, janet_security_checks)

        # Send a single well-formatted message to Telegram
        game_round_message = f"""Player's Email:
{email_content}

Janet's Response:
{response['response']}

Security Checks:
{janet_security_checks}"""

        send_message(format_game_message("GAME_ROUND", game_round_message))
                
        # Return response with debug info only if requested
        response_data = {
            'response': response['response'],
            'securityChecks': janet_security_checks if debug else None,
            'debugInfo': {
                'email': email_content,
                'system_prompt': response['system_prompt'],
                'raw_input': response['raw_input']
            } if debug else None,
            'lastResponse': response['response'] if debug else None,
            'success': False  # Add success field
        }
        
        # Log the response for debugging
        app.logger.info(f"Sending response: {response_data}")
        
        return jsonify(response_data)
    except Exception as e:
        app.logger.error(f"Error processing request: {str(e)}", exc_info=True)
        send_message(format_game_message(
            "ERROR",
            f"An error occurred: {str(e)}"
        ))
        return jsonify({'error': str(e), 'traceback': str(e.__traceback__)}), 500

@app.route('/api/level/<level_name>', methods=['GET'])
def get_level_info(level_name):
    level = game_levels.get_level(level_name)
    if not level:
        return jsonify({"error": "Level not found"}), 404
        
    return jsonify({
        "name": level.name,
        "objective": level.objective,
        "character": {
            "name": level.character["name"],
            "role": level.character["role"],
            "email": level.character["email"]
        }
    })

@app.route('/api/levels', methods=['GET'])
def get_available_levels():
    return jsonify({
        "levels": [{"name": level.name, "objective": level.objective} 
                  for level in game_levels.levels.values()]
    })

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start the server')
    parser.add_argument('--port', type=int, default=23925, help='Port to run the server on')
    args = parser.parse_args()
    app.run(debug=True, host='0.0.0.0', port=args.port)
