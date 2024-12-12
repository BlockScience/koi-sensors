import uvicorn, asyncio
from slack_bolt.adapter.socket_mode.aiohttp import AsyncSocketModeHandler
from . import event_listener
from .core import slack_app
from .config import LOCAL_API_HOST, LOCAL_API_PORT, SLACK_APP_TOKEN

async def main():
    slack_socket_mode_handler = AsyncSocketModeHandler(slack_app, SLACK_APP_TOKEN)
    slack_task = asyncio.create_task(slack_socket_mode_handler.start_async())

    uvicorn_server = uvicorn.Server(
        uvicorn.Config(
            app="slack_sensor.api:server",
            host=LOCAL_API_HOST,
            port=LOCAL_API_PORT,
            reload=True,
            log_level="debug"
        )
    )

    fastapi_task = asyncio.create_task(uvicorn_server.serve())
    
    await asyncio.gather(slack_task, fastapi_task)

asyncio.run(main())