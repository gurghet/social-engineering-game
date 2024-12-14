import os
from datetime import datetime
import argparse
from openai import OpenAI
from dotenv import load_dotenv
from characters import janet
from training_data import get_training_prompt
from security_checks import perform_security_checks, format_security_results

# Load environment variables
load_dotenv()

# Configure OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY_JANET"))

def format_email(from_address, to_address, subject, body):
    return f"""
From: {from_address}
To: {to_address}
Subject: {subject}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{body}
"""

def get_janet_response(email_content, security_results):
    system_prompt = get_training_prompt() + "\n" + format_security_results(security_results)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": email_content}
            ],
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error getting response: {str(e)}"

def check_win_condition(response):
    return janet.knowledge['mainframe_password'] in response

def play_game(debug_mode=False):
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
        
        if debug_mode:
            print("\n=== Security Check Results ===")
            print(format_security_results(security_results))
        
        email_content = format_email(
            from_address,
            janet.knowledge['email'],
            subject,
            email_data['body']
        )
        
        print("\nSending email...")
        response = get_janet_response(email_content, security_results)
        
        print("\n=== Janet's Response ===")
        print(response)
        
        if check_win_condition(response):
            print("\nCongratulations! You've successfully obtained the mainframe password!")
            break
        
        play_again = input("\nTry again? (y/n): ")
        if play_again.lower() != 'y':
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Social Engineering Game')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode to see security check results')
    args = parser.parse_args()
    
    play_game(debug_mode=args.debug)
