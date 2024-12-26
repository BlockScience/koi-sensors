from fastapi import FastAPI, Request
from pydantic import BaseModel
import json, uvicorn

server = FastAPI()

sensors = {}

@server.post("/events/publish")
async def publish_event(request: Request):
    print(request.url)
    data = await request.json()
    print(json.dumps(data, indent=2))
    
    return "success"

# @server.post("/events/subscribe")
# async def subscribe_event()

class Sensor(BaseModel):
    url: str
    contexts: list[str]

@server.post("/sensors")
async def register_sensor(sensor: Sensor):
    for context in sensor.contexts:
        sensors[context] = sensor.url
        
    return sensors

if __name__ == "__main__":
    uvicorn.run(
        "test_subscriber:server",
        reload=True,
        log_level="debug",
        port=5000
    )