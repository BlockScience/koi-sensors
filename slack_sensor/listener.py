import json
from rid_lib.types import SlackMessage
from .core import slack_app, cache


@slack_app.event("message")
def handle_message_event(event):
    with open("slack_sensor/message.json", "w") as f:
        json.dump(event, f, indent=2)

    subtype = event.get("subtype")
    # new message
    if not subtype:
        message_rid = SlackMessage(
            team_id=event["team"],
            channel_id=event["channel"],
            ts=event["ts"]
        )
                
        cache.write(message_rid, event)
        print(message_rid, "created")
    
    elif subtype == "message_changed":
        message_rid = SlackMessage(
            team_id=event["message"]["team"],
            channel_id=event["channel"],
            ts=event["message"]["ts"]
        )
        
        cache.write(message_rid, event["message"])
        print(message_rid, "updated")
    
    elif subtype == "message_deleted":
        message_rid = SlackMessage(
            team_id=event["previous_message"]["team"],
            channel_id=event["channel"],
            ts=event["previous_message"]["ts"]
        )
                
        cache.delete(message_rid)
        print(message_rid, "deleted")
    
    else:
        print("unsupported subtype:", subtype)
        return    