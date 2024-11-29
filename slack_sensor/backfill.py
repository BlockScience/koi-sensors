import time
from slack_sdk.errors import SlackApiError
from rid_lib.types import SlackMessage
from .core import slack_app, cache


def auto_retry(function, **params):
    try:
        return function(**params)
    except SlackApiError as e:
        if e.response["error"] == "ratelimited":
            retry_after = int(e.response.headers["Retry-After"])
            print(f"timed out, waiting {retry_after} seconds")
            time.sleep(retry_after)
            return function(**params)
        else:
            print("unknown error", e)

def run(channel_ids=[]):
    team = slack_app.client.team_info().data["team"]
    team_id = team["id"]

    if channel_ids:
        channels = [{"id": cid} for cid in channel_ids]
    else: channels = []
    
    # get list of channels
    channel_cursor = None
    while not channels or channel_cursor:
        result = slack_app.client.conversations_list(cursor=channel_cursor).data
        channels.extend(result["channels"])
        channel_cursor = result.get("response_metadata", {}).get("next_cursor")

    for channel in channels:
        channel_id = channel["id"]
        
        print(channel_id)

        # get list of messages in channel
        message_cursor = None
        messages = []
        while not messages or message_cursor:
            result = auto_retry(slack_app.client.conversations_history,
                channel=channel_id,
                limit=500,
                cursor=message_cursor
            )
            
            messages.extend(result["messages"])
            if result["has_more"]:
                message_cursor = result["response_metadata"]["next_cursor"]
            else:
                message_cursor = None


        for message in messages:
            message_rid = SlackMessage(team_id, channel_id, message["ts"])
            
            if message.get("subtype") is None:
                cache.write(message_rid, message)
                print(message_rid)
            
            thread_ts = message.get("thread_ts")
            
            # ignore threaded messages sent to channel (double counted within thread)
            if thread_ts and (thread_ts != message["ts"]):
                print("🤫", message_rid)
                continue

            if thread_ts:
                threaded_message_cursor = None
                threaded_messages = []
                while not threaded_messages or threaded_message_cursor:
                    result = auto_retry(slack_app.client.conversations_replies,
                        channel=channel_id,
                        ts=thread_ts,
                        limit=500,
                        cursor=threaded_message_cursor
                    )
                            
                    threaded_messages.extend(result["messages"])
                    
                    if result["has_more"]:
                        threaded_message_cursor = result["response_metadata"]["next_cursor"]
                    else:
                        threaded_message_cursor = None
                
                # don't double count thread parent message
                for threaded_message in threaded_messages[1:]:
                    threaded_message_rid = SlackMessage(team_id, channel_id, threaded_message["ts"])
                    if threaded_message.get("subtype") is None:
                        cache.write(threaded_message_rid, threaded_message)
                        print(threaded_message_rid)
                    
        print()
