from fastapi import FastAPI, Request, Query
from rid_lib import RID
from .core import slack_app, slack_handler, cache

server = FastAPI()



@server.post("/slack/listener")
async def slack_listener(request: Request):
    return await slack_handler.handle(request)
    
@server.get("/resource")
async def get_resource(rid: str = Query(...)):
    rid_obj = RID.from_string(rid)
    
    data = cache.read(rid_obj)
    
    if data is None:
        response = slack_app.client.conversations_replies(
            channel=rid_obj.channel_id,
            ts=rid_obj.ts
        )
        data = response["messages"][0]
        cache.write(rid_obj, data)
    
    return data