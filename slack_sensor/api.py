import httpx
import json
import asyncio
from fastapi import FastAPI, Request, Query, Depends, APIRouter
from pydantic import BaseModel
from contextlib import asynccontextmanager
from rid_lib import RID
from rid_lib.ext import CacheBundle, Manifest
from .core import async_slack_handler, cache
from .actions import dereference
from .auth import api_key_header
from .config import COORDINATOR_NODE_URL, COORDINATOR_API_HEADER, PUBLISHER_ID, LAST_PROCESSED_TS, OBSERVING_CHANNELS
from .backfill import backfill_messages


@asynccontextmanager
async def lifespan(server: FastAPI):
    print(LAST_PROCESSED_TS)
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            COORDINATOR_NODE_URL + f"/profiles/publisher/{PUBLISHER_ID}",
            headers=COORDINATOR_API_HEADER,
            json={
                "contexts": [
                    "orn:slack.message",
                    "orn:slack.user",
                    "orn:slack.workspace",
                    "orn:slack.channel"
                ],
                "url": "https://koi-dev.lukvmil.com/slack_sensor"
            }
        )
        data = resp.json()
        print(json.dumps(data, indent=2))
    
    asyncio.create_task(
        backfill_messages(
            channel_ids=OBSERVING_CHANNELS,
            after=LAST_PROCESSED_TS))
    yield

server = FastAPI(lifespan=lifespan)

router = APIRouter(
    dependencies=[Depends(api_key_header)]
)

@server.post("/slack/listener")
async def slack_listener(request: Request):
    # handled in listener.py
    return await async_slack_handler.handle(request)
    
@router.get("/object")
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

@router.post("/objects")
async def post_objects(resources: RetrieveObjects):
    return {
        rid_str: cache.read(RID.from_string(rid_str))
        for rid_str in resources.rids
    }
    

@router.get("/rids")
async def get_rids():
    return [
        str(rid) for rid in cache.read_all_rids()
    ]
    
server.include_router(router)
