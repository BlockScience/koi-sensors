from .rid_extension import HackMDNote
from . import hackmd_api

def dereference(note: HackMDNote):
    return hackmd_api.request(f"/notes/{note.note_id}")