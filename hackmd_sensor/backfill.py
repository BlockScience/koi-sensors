import httpx
from .rid_types import HackMDNote
from . import coordinator, hackmd_api
from .config import COORDINATOR_NODE_URL, COORDINATOR_API_HEADER, PUBLISHER_ID

def run(team_path="blockscience"):
    httpx.post(
        COORDINATOR_NODE_URL + "/profiles/publisher/" + PUBLISHER_ID,
        headers=COORDINATOR_API_HEADER,
        json={
            "url": "http://127.0.0.1:8000",
            "contexts": [
                "orn:hackmd.note"
            ]
        }
    )
    
    notes = hackmd_api.request(f"/teams/{team_path}/notes")

    for note in notes:
        note_rid = HackMDNote(note["id"])
        coordinator.report_obj_discovery(note_rid, note)
        
if __name__ == "__main__":
    run()