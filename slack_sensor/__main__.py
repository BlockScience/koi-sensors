import uvicorn

uvicorn.run(
    "slack_sensor:server",
    reload=True,
    log_level="debug"
)