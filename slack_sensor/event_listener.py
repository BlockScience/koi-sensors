import json
from rid_lib.types import SlackMessage
from .core import slack_app
from . import coordinator
from .config import OBSERVING_CHANNELS


@slack_app.event("message")
async def handle_message_event(event):
    # with open("slack_sensor/message.json", "w") as f:
    #     json.dump(event, f, indent=2)

    subtype = event.get("subtype")
    # new message
    if not subtype:
        message_rid = SlackMessage(
            team_id=event["team"],
            channel_id=event["channel"],
            ts=event["ts"]
        )
        
        if message_rid.channel_id not in OBSERVING_CHANNELS:
            return
        
        # normalize to non event message structure
        data = event
        del data["channel"]
        del data["event_ts"]
        del data["channel_type"]
        
        await coordinator.handle_obj_discovery(message_rid, data)
    
    elif subtype == "message_changed":
        message_rid = SlackMessage(
            team_id=event["message"]["team"],
            channel_id=event["channel"],
            ts=event["message"]["ts"]
        )
        # normalize to non event message structure
        data = event["message"]
        del data["source_team"]
        del data["user_team"]
        
        await coordinator.handle_obj_discovery(message_rid, data)
    
    elif subtype == "message_deleted":
        message_rid = SlackMessage(
            team_id=event["previous_message"]["team"],
            channel_id=event["channel"],
            ts=event["previous_message"]["ts"]
        )
                
        await coordinator.handle_obj_deletion(message_rid)
    
    else:
        print("unsupported subtype:", subtype)
        return    