from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from janet import janet
import os
from security_checks import SecurityChecker

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize rate limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["1 per second"],
    storage_uri="memory://"
)

# Debug mode from environment variable, defaults to False
DEBUG_MODE = True  # Force debug mode for development

@app.route('/send_email', methods=['POST'])
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
        
        # Debug print
        print("Response:", janet_response)
        print("Security checks:", janet_security_checks)
        
        # Check if password was obtained by looking for the exact format in the response
        success = "Password: " in str(janet_response) and any(
            f"Password: {password}" in str(janet_response)
            for password in janet.get_level_passwords()
        )

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
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=DEBUG_MODE, port=23925)
