from pathlib import Path

from dotenv import load_dotenv


def load_env():
    """
    Load the environment variables from the .env file.
    """
    # Project root (when this file is src/middleware/load_env.py)
    load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")