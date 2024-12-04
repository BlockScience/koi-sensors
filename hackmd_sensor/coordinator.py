from rid_lib import RID
from .core import cache
from .actions import dereference

def report_obj_discovery(rid: RID, data: dict):
    if cache.exists(rid):
        obj = cache.read(rid)
        if data["lastChangedAt"] > obj.data["lastChangedAt"]:
            print(rid, "[UPDATED]")
            data = dereference(rid)
            if data is not None:
                cache.write(rid, data)
        else:
            print(rid, "[NO CHANGE]")
    else:
        print(rid, "[NEW]")
        data = dereference(rid)
        if data is not None:
            cache.write(rid, data)