from fastapi import FastAPI, Request, Query
from contextlib import asynccontextmanager
from rid_lib import RID
from .core import slack_handler, cache
from .actions import dereference


@asynccontextmanager
async def lifespan(server: FastAPI):
    import time
    time.sleep(10)
    print("start")
    yield
    print("end")

server = FastAPI(lifespan=lifespan)


@server.post("/slack/listener")
async def slack_listener(request: Request):
    # handled in listener.py
    return await slack_handler.handle(request)
    
@server.get("/resource")
async def get_resource(rid: str = Query(...)):
    rid_obj = RID.from_string(rid)
    
    data = cache.read(rid_obj)
    
    if data is None:
        data = dereference(rid_obj)
        if data is not None:
            cache.write(rid_obj, data)
    
    return data