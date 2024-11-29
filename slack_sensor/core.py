from dotenv import load_dotenv
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from simple_cache import CacheInterface

load_dotenv()

slack_app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"],
)

slack_socket_mode_handler = SocketModeHandler(slack_app, os.environ["SLACK_APP_TOKEN"])

cache = CacheInterface("slack_sensor/cache")
