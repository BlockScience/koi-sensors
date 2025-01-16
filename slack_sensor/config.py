from dotenv import load_dotenv
import os
import json

load_dotenv("slack_sensor/.env")

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
SLACK_APP_TOKEN= os.environ["SLACK_APP_TOKEN"]

LOCAL_API_HOST = "localhost"
LOCAL_API_PORT = 8000
LOCAL_API_URL = f"http://{LOCAL_API_HOST}:{LOCAL_API_PORT}"

COORDINATOR_NODE_URL = "http://localhost:5000"
COORDINATOR_API_KEY = os.environ["COORDINATOR_API_KEY"]
COORDINATOR_API_HEADER = {
    "X-API-Key": COORDINATOR_API_KEY
}
PUBLISHER_ID = "CDph6lHPtMOdQ4AUmVLOPA"

AUTH_JSON_PATH = "auth.json"

OBSERVING_CHANNELS = [
    "C0593RJJ2CW",
    "C082YTFAA83"
]

def load_state():
    try:
        with open("state.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "ts": 0
        }

LAST_PROCESSED_TS = load_state()["ts"]            

def update_state(ts):
    global LAST_PROCESSED_TS
    if ts < LAST_PROCESSED_TS: return
    
    print("updated", LAST_PROCESSED_TS)
    
    with open("state.json", "w") as f:
        json.dump({
            "ts": ts
        }, f)
    LAST_PROCESSED_TS = ts
            
