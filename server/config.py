from dotenv import load_dotenv
import os

def load_env():
    """Load environment variables from .env files if not already set in environment"""
    # Don't override existing environment variables
    load_dotenv_kwargs = {"override": False}
    
    # Try ~/.janet-secrets/.env first
    home_env_path = os.path.expanduser("~/.janet-secrets/.env")
    if os.path.exists(home_env_path):
        load_dotenv(home_env_path, **load_dotenv_kwargs)
    
    # Then try project root .env
    project_env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    if os.path.exists(project_env_path):
        load_dotenv(project_env_path, **load_dotenv_kwargs)

# Load environment variables when the module is imported
load_env()
