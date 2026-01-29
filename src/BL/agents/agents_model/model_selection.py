import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model, BaseChatModel
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
# From: src/BL/agents/agents_model/model_selection.py -> src/.env
env_path = Path(__file__).parent.parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


def get_dynamic_model_instance(model_name: str, temperature: float = 0.0) -> Optional[BaseChatModel]:
    """Initialize and return the chat model instance."""
    try:
        if model_name == "":
            model_name = "gpt-4o"
        dynamic_model = init_chat_model(model=model_name, temperature=temperature)
        if dynamic_model is None:
            dynamic_model = ChatOpenAI(model="gpt-4o", temperature=0)
        return dynamic_model
    except Exception as e:
        return None
    
def get_default_model_name(model_name: str = '') -> str:
    if model_name == '':
        model_name = 'gpt-4o-mini'
    return model_name
