from fastapi import FastAPI, Request, Query
from pydantic import BaseModel
from contextlib import asynccontextmanager
from rid_lib import RID
from .core import slack_handler, cache
from .actions import dereference


@asynccontextmanager
async def lifespan(server: FastAPI):
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

class RetrieveResources(BaseModel):
    rids: list[str]

@server.post("/resource/retrieve")
async def post_resource_retrieve(resources: RetrieveResources):
    return {
        rid_str: cache.read(RID.from_string(rid_str))
        for rid_str in resources.rids
    }
    

@server.get("/resource/list")
async def get_resource_list():
    return [
        str(rid) for rid in cache.read_all_rids()
    ]