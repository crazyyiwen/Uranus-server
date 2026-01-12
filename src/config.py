import os
import configparser
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    def __init__(self):
        try:
            # self.envparams = {
            #     "TCSUrl" : os.environ['TCSUrl'],
            #     "AppId" : os.environ['AppId'],
            #     "RegionId" : os.environ['RegionId'],
            #     "ACSClientId" : os.environ['ACSClientId'],
            #     "AppGroupId" : os.environ['AppGroupId']
            # }
            self.envparams = {
                "TCSUrl" : "https://internal-leoaksqc.gep.com/leo-storage-tcsservice",
                "AppId" : 1029,
                "RegionId" : 1,
                "ACSClientId" : "86FB623E155A723CE18EE8946AC1A5FCABBA116652521ACBBC012BDA8485B9A2",
                "AppGroupId" : 3,
                "APP_NAME":"leo-p2p-common-ai"
            }

            self.agent_env_params = {
                "TAVILY_API_KEY": os.environ.get("TAVILY_API_KEY", ""),
                "ANTHROPIC_API_KEY": os.environ.get("ANTHROPIC_API_KEY", ""),
                "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", ""),
                "LANGSMITH_PROJECT": os.environ.get("LANGSMITH_PROJECT", "deep-agents-from-scratch"),
                "LANGCHAIN_TRACING_V2": os.environ.get("LANGCHAIN_TRACING_V2", "True").lower() == "true",
                "LANGCHAIN_ENDPOINT": os.environ.get("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com"),
                "LANGCHAIN_API_KEY": os.environ.get("LANGCHAIN_API_KEY", "")
            }

            self.envparams = self.envparams | self.agent_env_params

        except KeyError:
            config = configparser.ConfigParser()
            dir_path = os.path.dirname(os.path.realpath(__file__))
            ini_path = os.path.join(dir_path, "env_config.ini")
            config.read(ini_path)
            self.envparams = {
                "TCSUrl" : config['env_dev']['TCSUrl'],
                "AppId" : config['env_dev']['AppId'],
                "RegionId" : config['env_dev']['RegionId'],
                "ACSClientId" : config['env_dev']['ACSClientId'],
                "AppGroupId" : config['env_dev']['AppGroupId']
            }
