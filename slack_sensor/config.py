from dotenv import load_dotenv
import os

load_dotenv("slack_sensor/.env")

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
SLACK_APP_TOKEN= os.environ["SLACK_APP_TOKEN"]

LOCAL_API_HOST = "127.0.0.1"
LOCAL_API_PORT = 8000
LOCAL_API_URL = f"http://{LOCAL_API_HOST}:{LOCAL_API_PORT}"