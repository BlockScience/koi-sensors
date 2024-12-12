from slack_bolt import App
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi import SlackRequestHandler
from simple_cache import CacheInterface
from .config import *

slack_app = AsyncApp(
    token=SLACK_BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET,
)

slack_handler = SlackRequestHandler(slack_app)


cache = CacheInterface("slack_sensor/cache")