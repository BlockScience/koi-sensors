import httpx
from jsondiff import diff
from rid_lib import RID, Manifest
from rid_lib.utils import hash_json
from .core import cache
from .config import COORDINATOR_NODE_URL


async def broadcast_event(rid: RID, event_type: str, manifest: Manifest | None = None):
    event = {
        "rid": str(rid),
        "type": event_type
    }
    
    if manifest:
        event["manifest"] = manifest.to_dict()
    
    async with httpx.AsyncClient() as client:
        await client.post(
            COORDINATOR_NODE_URL + "/events/publish",
            json=event
        )
    

async def handle_obj_discovery(rid: RID, data: dict):
    if cache.exists(rid):
        obj = cache.read(rid)
        if obj.manifest.sha256_hash == hash_json(data):
            # print(rid, "[NO CHANGE]")
            ...
        else:
            print(rid, "[UPDATED]")
            print(diff(obj.data, data))
            
            obj = cache.write(rid, data)
            
            await broadcast_event(rid, "UPDATED", obj.manifest)
    else:
        print(rid, "[NEW]")
        obj = cache.write(rid, data)

        await broadcast_event(rid, "NEW", obj.manifest)
    
async def handle_obj_deletion(rid: RID):
    print(rid, "[DELETED]")
    cache.delete(rid)
    
    
    await broadcast_event(rid, "DELETED")