from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.adapter.fastapi import SlackRequestHandler
from simple_cache import CacheInterface
from .config import *

slack_app = App(
    token=SLACK_BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET,
)

slack_handler = SlackRequestHandler(slack_app)

slack_socket_mode_handler = SocketModeHandler(slack_app, SLACK_APP_TOKEN)

cache = CacheInterface("slack_sensor/cache")
