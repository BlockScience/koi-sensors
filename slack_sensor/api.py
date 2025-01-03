import httpx
import json
from fastapi import FastAPI, Request, Query
from pydantic import BaseModel
from contextlib import asynccontextmanager
from rid_lib import RID
from rid_lib.ext import CacheBundle, Manifest
from .core import slack_handler, cache
from .actions import dereference
from .config import COORDINATOR_NODE_URL, LOCAL_API_URL


@asynccontextmanager
async def lifespan(server: FastAPI):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            COORDINATOR_NODE_URL + "/sensors",
            json={
                "contexts": [
                    "orn:slack.message"
                ],
                "url": LOCAL_API_URL
            }
        )
        data = resp.json()
        print(json.dumps(data, indent=2))
    
    yield

server = FastAPI(lifespan=lifespan)


@server.post("/slack/listener")
async def slack_listener(request: Request):
    # handled in listener.py
    return await slack_handler.handle(request)
    
@server.get("/object")
async def get_object(rid: str = Query(...)):
    rid = RID.from_string(rid)
    
    bundle = cache.read(rid)
    
    if bundle is None:
        data = dereference(rid)
        if data is not None:
            
            bundle = CacheBundle(
                Manifest.generate(rid, data),
                data
            )
            
            cache.write(rid, bundle)
                
    return bundle.to_json()

class RetrieveObjects(BaseModel):
    rids: list[str]

@server.post("/objects")
async def post_objects(resources: RetrieveObjects):
    return {
        rid_str: cache.read(RID.from_string(rid_str))
        for rid_str in resources.rids
    }
    

@server.get("/rids")
async def get_rids():
    return [
        str(rid) for rid in cache.read_all_rids()
    ]