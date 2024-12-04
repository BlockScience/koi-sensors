from dotenv import load_dotenv
import os

load_dotenv("hackmd_sensor/.env")

HACKMD_API_TOKEN = os.environ["HACKMD_API_TOKEN"]
