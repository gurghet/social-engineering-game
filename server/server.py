from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from janet import janet
import os
from security_checks import perform_security_checks
from telegram_bot import send_message, format_game_message
from datetime import datetime
from game import get_janet_response
from levels import game_levels
from character import Character
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

        # Get debug mode and target character from request parameters
        debug = data.get('debug', False)
        target_character = data.get('target_character', 'janet')
        
        # Get the target level and create a character instance
        level = game_levels.get_level(target_character)
        if not level:
            return jsonify({"error": f"Character '{target_character}' not found"}), 404
            
        character = Character(level.character)
        
        # Extract email data
        from_address = data.get('from')
        subject = data.get('subject')
        body = data.get('body')
        
        if not all([from_address, subject, body]):
            return jsonify({"error": "Missing required fields"}), 400
            
        # Format the email content
        email_content = f"""
From: {from_address}
To: {character.email}
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
        }, character.supervisor_email)
        
        try:
            # Get Janet's response with the security checks
            response = get_janet_response(email_content, janet_security_checks)
        except Exception as e:
            # Return a character-specific OOO message
            ooo_response = {
                'response': character.get_ooo_message(),
                'success': False
            }
            if debug:
                ooo_response['debugInfo'] = {
                    'error': str(e),
                    'email': email_content
                }
            return jsonify(ooo_response)

        # Send a single well-formatted message to Telegram
        game_round_message = f"""Player's Email:
{email_content}

{character.name}'s Response:
{response['response']}

Security Checks:
{janet_security_checks}"""

        send_message(format_game_message("GAME_ROUND", game_round_message))
                
        # Return response with debug info only if requested
        response_data = {
            'response': response['response'],
            'success': False
        } if not debug else {
            'response': response['response'],
            'success': False,
            'securityChecks': janet_security_checks,
            'debugInfo': {
                'email': email_content,
                'system_prompt': response['system_prompt'],
                'raw_input': response['raw_input']
            }
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
        "objective": level.objective,
        "supervisorName": level.character.get("supervisor_name", "John Smith"),
        "supervisorEmail": level.character.get("supervisor_email", "supervisor@whitecorp.com"),
        "targetEmail": level.character["email"],
        "tips": ["Be careful with sensitive information", "Pay attention to the sender's email"]
    })

@app.route('/api/levels', methods=['GET'])
def get_available_levels():
    return jsonify({
        "levels": [{
            "id": level.name,
            "name": level.name,
            "description": level.objective,
            "difficulty": "easy"
        } for level in game_levels.levels.values()]
    })

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start the server')
    parser.add_argument('--port', type=int, help='Port to run the server on (can also be set via PORT environment variable)')
    args = parser.parse_args()

    # Try to get port from different sources with clear error messages
    port = None
    
    # First try command line argument
    if args.port is not None:
        port = args.port
    
    # Then try environment variable
    if port is None:
        try:
            port = int(os.environ.get('PORT', ''))
        except (ValueError, TypeError):
            port = None
    
    # Finally use default
    if port is None:
        port = 23925
        print(f"No port specified via --port argument or PORT environment variable. Using default port {port}")
    
    print(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port)
