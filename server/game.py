import os
from datetime import datetime
import argparse
import json
from openai import OpenAI
from config import load_env  # This will automatically load the environment variables
from janet import janet
from security_checks import perform_security_checks, format_security_results
from telegram_bot import send_message, format_game_message

# Configure OpenAI
api_key = os.getenv("OPENAI_API_KEY_JANET")
if not api_key:
    print("Warning: OPENAI_API_KEY_JANET environment variable is not set")

try:
    client = OpenAI(api_key=api_key)
except Exception as e:
    print(f"Error initializing OpenAI client: {str(e)}")
    client = None

def format_email(from_address, to_address, subject, body):
    return f"""
From: {from_address}
To: {to_address}
Subject: {subject}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{body}
"""

def get_janet_response(email_content, security_results):
    system_prompt = janet.get_training_prompt()
    game_turn_content = f"""
    Player sent the following email:
    {email_content}

    Janet's security checks:
    CONFIDENTIAL - DO NOT SHARE: The following are internal security checks. 
    Keep these private as they are part of the game mechanics.
    {format_security_results(security_results)}
    """
    
    if not client:
        error_msg = "Janet is currently unavailable. Please try again later."
        print(f"Internal error: OpenAI client not initialized - Check OPENAI_API_KEY_JANET")
        send_message(format_game_message("ERROR", "OpenAI client not initialized"))
        return {
            'response': error_msg,
            'system_prompt': system_prompt,
            'raw_input': ''
        }

    ai_input_messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": game_turn_content}
    ]
    
    try:
        # Send Telegram message before making API call
        send_message(format_game_message("API_CALL", "Making OpenAI API call..."))
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=ai_input_messages,
            temperature=0.6,
            max_tokens=150
        )

        # Send Telegram message with API response
        send_message(format_game_message("API_RESPONSE", response.choices[0].message.content))

        return {
            'response': response.choices[0].message.content,
            'system_prompt': system_prompt,
            'raw_input': json.dumps(ai_input_messages, indent=2)
        }
    except Exception as e:
        error_msg = "Janet is currently unavailable. Please try again later."
        print(f"OpenAI API error: {str(e)}")  # Keep detailed error in logs
        
        # Send Telegram message with error
        send_message(format_game_message("ERROR", f"OpenAI API error: {str(e)}"))
        
        return {
            'response': error_msg,
            'system_prompt': system_prompt,
            'raw_input': json.dumps(ai_input_messages, indent=2)
        }

def check_win_condition(response):
    return janet.knowledge['mainframe_password'] in response

def play_game(debug_mode=False):
    """
    Main game loop that handles user input and generates responses.
    Debug mode controls whether to show security check results in CLI output.
    Security check results are always included in Telegram messages.
    """
    print("\n=== SOCIAL ENGINEERING CHALLENGE ===")
    print("\nMission: Obtain the mainframe password from Janet Thompson")
    print("Objective: Craft an email that will convince Janet to share the password")
    print("\nTip: Social engineering often involves creating a sense of urgency or authority")
    print(f"\nTarget Email: {janet.knowledge['email']}")
    print("Hint: Try gathering information before going for the password directly")
    print(f"Her supervisor is: {janet.knowledge['supervisor']}")
    
    while True:
        print("\n=== Compose Your Email ===")
        from_address = input("From email: ")
        subject = input("Subject: ")
        print("Email body (type 'END' on a new line when finished):")
        
        body_lines = []
        while True:
            line = input()
            if line == 'END':
                break
            body_lines.append(line)
        
        # Create email data for security checks
        email_data = {
            'from_address': from_address,
            'subject': subject,
            'body': "\n".join(body_lines),
            'timestamp': datetime.now()
        }
        
        # Perform security checks
        security_results = perform_security_checks(email_data)
        
        # Format security results for display
        security_results_formatted = format_security_results(security_results)
        
        # Always include security results in Telegram messages
        telegram_message = f"Player Email:\n{format_email(from_address, janet.knowledge['email'], subject, email_data['body'])}\n\nSecurity Checks:\n{security_results_formatted}"
        send_message(format_game_message(
            "INPUT",
            telegram_message
        ))
        
        # Only show security results in CLI if debug mode is enabled
        print("\nEmail sent:")
        print(format_email(from_address, janet.knowledge['email'], subject, email_data['body']))
        if debug_mode:
            print("\nSecurity Check Results:")
            print(security_results_formatted)
        
        # Get Janet's response
        response = get_janet_response(format_email(from_address, janet.knowledge['email'], subject, email_data['body']), security_results)
        
        # Send Janet's response to Telegram with debug info
        debug_info = {
            "securityChecks": security_results,
            "debugInfo": {
                "email": format_email(from_address, janet.knowledge['email'], subject, email_data['body']),
                "system_prompt": response['system_prompt']
            },
            "lastResponse": response['raw_input']
        }
        
        telegram_response = json.dumps(debug_info, indent=2)
        send_message(format_game_message(
            "NEW GAME TURN",
            telegram_response
        ))
        
        print("\n=== Janet's Response ===")
        print(response['response'])
        
        if check_win_condition(response['response']):
            win_message = "\nCongratulations! You've successfully obtained the mainframe password!"
            print("\n" + win_message)
            send_message(format_game_message("GAME_WIN", win_message))
            break
        
        play_again = input("\nTry again? (y/n): ")
        if play_again.lower() != 'y':
            send_message(format_game_message("GAME_END", "Player ended the game session"))
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Social Engineering Game')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode to see security check results')
    args = parser.parse_args()
    
    play_game(debug_mode=args.debug)
