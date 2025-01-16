import httpx
from rid_lib import RID
from rid_lib.ext import Event, EventType
from .core import cache
from .actions import dereference
from .config import COORDINATOR_NODE_URL, PUBLISHER_ID, COORDINATOR_API_HEADER

def broadcast_event(event: Event):
    httpx.post(
        COORDINATOR_NODE_URL + "/events/publish/" + PUBLISHER_ID,
        headers=COORDINATOR_API_HEADER,
        json=[event.to_json()]
    )

def report_obj_discovery(rid: RID, data: dict):
    if cache.exists(rid):
        obj = cache.read(rid)        
        if data["lastChangedAt"] > obj.contents["lastChangedAt"]:
            print(rid, "[UPDATED]")
            data = dereference(rid)
            if data is not None:
                bundle = cache.bundle_and_write(rid, data)
                
                broadcast_event(
                    Event(rid, EventType.UPDATE, bundle.manifest)
                )
        else:
            print(rid, "[NO CHANGE]")
    else:
        print(rid, "[NEW]")
        data = dereference(rid)
        if data is not None:
            bundle = cache.bundle_and_write(rid, data)
            
            broadcast_event(
                Event(rid, EventType.NEW, bundle.manifest)
            )