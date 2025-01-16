from slack_bolt import App
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler
from rid_lib.ext import Cache
from .config import *

slack_app = AsyncApp(
    token=SLACK_BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET,
)

async_slack_handler = AsyncSlackRequestHandler(slack_app)


cache = Cache("slack_sensor/cache")

from . import event_listener