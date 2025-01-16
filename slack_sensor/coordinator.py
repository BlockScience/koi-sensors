import httpx
from jsondiff import diff
from rid_lib import RID
from rid_lib.ext import Manifest, Event, EventType, CacheBundle, utils
from .core import cache
from .config import COORDINATOR_NODE_URL, PUBLISHER_ID, COORDINATOR_API_HEADER, update_state


async def broadcast_event(event: Event):
    async with httpx.AsyncClient() as client:
        await client.post(
            COORDINATOR_NODE_URL + "/events/publish/" + PUBLISHER_ID,
            headers=COORDINATOR_API_HEADER,
            json=[event.to_json()]
        )
    

async def handle_obj_discovery(rid: RID, data: dict):
    update_state(ts=float(rid.ts))
    if cache.exists(rid):
        bundle = cache.read(rid)
        if bundle.manifest.sha256_hash == utils.sha256_hash_json(data):
            # print(rid, "[NO CHANGE]")
            ...
        else:
            print(rid, "[UPDATED]")
            print(diff(bundle.contents, data))
            
            bundle = CacheBundle(
                manifest=Manifest.generate(rid, data),
                contents=data
            )
            cache.write(rid, bundle)
            
            await broadcast_event(
                Event(rid, EventType.UPDATE, bundle.manifest))
    else:
        print(rid, "[NEW]")
        bundle = CacheBundle(
            manifest=Manifest.generate(rid, data),
            contents=data
        )
        cache.write(rid, bundle)

        await broadcast_event(
            Event(rid, EventType.NEW, bundle.manifest))
    
async def handle_obj_deletion(rid: RID):
    print(rid, "[DELETED]")
    cache.delete(rid)
    
    await broadcast_event(
        Event(rid, EventType.UPDATE))