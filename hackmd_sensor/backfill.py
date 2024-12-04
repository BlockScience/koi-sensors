
from .rid_extension import HackMDNote
from . import coordinator, hackmd_api

def run(team_path="blockscience"):
    notes = hackmd_api.request(f"/teams/{team_path}/notes")

    for note in notes:
        note_rid = HackMDNote(note["id"])
        coordinator.report_obj_discovery(note_rid, note)
    
    
        
if __name__ == "__main__":
    run()