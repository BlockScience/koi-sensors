from rid_lib import RID
from simple_cache import hash_json
from .core import cache


def report_obj_discovery(rid: RID, data: dict):
    if cache.exists(rid):
        obj = cache.read(rid)
        if obj.meta["sha256_hash"] == hash_json(data):
            print(rid, "[NO CHANGE]")
        else:
            print(rid, "[UPDATED]")
            cache.write(rid, data)
    else:
        print(rid, "[NEW]")
        cache.write(rid, data)
    
def report_deleted_obj(rid: RID):
    print(rid, "[DELETED]")
    cache.delete(rid)