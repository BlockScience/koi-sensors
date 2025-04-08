import requests
import os
from rid_lib.ext import Event, EventType, CacheBundle

COORDINATOR_URL = "https://koi-dev.lukvmil.com/coordinator"
API_HEADER = {"X-API-Key": os.environ["COORDINATOR_API_KEY"]}

resp = requests.post(
    COORDINATOR_URL + f"/profiles/subscriber/c0tbDvvBAwtCvK3Hu-VPXQ",
    headers=API_HEADER,
    json={
        "sub_type": "poll",
        "contexts": [
            "orn:slack.message"
        ]
    }
)

sub_id = resp.json()["sub_id"]
print("Subscriber ID registered:", sub_id)

resp = requests.get(
    COORDINATOR_URL + "/profiles/publisher?context=orn:slack.message",
    headers=API_HEADER,
)

slack_sensor_profile = resp.json()[0]
slack_sensor_url = slack_sensor_profile["url"]

print("Remote sensor URL retrieved:", slack_sensor_url)

resp = requests.get(
    COORDINATOR_URL + f"/events/poll/{sub_id}",
    headers=API_HEADER
)

events = resp.json()
print(f"Processing {len(events)} events")

for event_json in events:
    event = Event.from_json(event_json)
    print(event.event_type, event.rid)
    
    if event.event_type in (EventType.NEW, EventType.UPDATE):
        resp = requests.get(
            slack_sensor_url + "/object?rid=" + str(event.rid),
            headers=API_HEADER
        )
        
        bundle_json = resp.json()
        bundle = CacheBundle.from_json(bundle_json)
        
        print(bundle.contents["text"])