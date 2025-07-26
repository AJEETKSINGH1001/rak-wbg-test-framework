import os
from dotenv import load_dotenv

# Force .env to load from the root directory of the project
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path=env_path)

class Config:
    BASE_URL = os.getenv("BASE_URL")
    PIPELINE_URL = f"{BASE_URL}pipeline"
    PORTFOLIO_URL = f"{BASE_URL}portfolio"
    TASKBOARD_URL = f"{BASE_URL}scrumboard/kanban"
    TEST_EMAIL = os.getenv("TEST_EMAIL")
    PASSWORD = os.getenv("PASSWORD")
