from fastapi import FastAPI, Request
from pydantic import BaseModel
import json, uvicorn, httpx
from rid_lib.ext import Event, CacheBundle

server = FastAPI()

sensors = {}

@server.post("/events/publish")
async def publish_event(request: Request):
    print(request.url)
    data = await request.json()
    print(json.dumps(data, indent=2))
    
    event = Event.from_json(data)
    print(event)
    
    remote_sensor = sensors[event.rid.context]
    
    resp = httpx.get(remote_sensor + f"/object?rid={event.rid}")
    
    bundle = CacheBundle.from_json(resp.json())
    
    print(bundle)
    
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
        "placeholder_coordinator:server",
        reload=True,
        log_level="debug",
        port=5000
    )