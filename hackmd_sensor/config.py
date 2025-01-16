from dotenv import load_dotenv
import os

load_dotenv("hackmd_sensor/.env")

HACKMD_API_TOKEN = os.environ["HACKMD_API_TOKEN"]

COORDINATOR_NODE_URL = "https://koi-dev.lukvmil.com/coordinator"
COORDINATOR_API_KEY = os.environ["COORDINATOR_API_KEY"]
COORDINATOR_API_HEADER = {
    "X-API-Key": COORDINATOR_API_KEY
}
PUBLISHER_ID = "Eew5p7F-mPjSSUtEJZk7SQ"