import json

from pywebpush import webpush
from pywebpush import WebPushException

try:
    push_data = {
        "subscription_info": {
            "endpoint": "https://fcm.googleapis.com/fcm/send/d2Vj2HXnWS0:"
            + "APA91bGW_si_MDp8h2g016QAZIZy3w5jecWOn4ZB1oWX3qESi9ROlxfNc_QHSb_"
            + "ELpzOGE5dRGwaa2M2rPGzFDZC63OV5962BH3747qg1bw2GkMVv3"
            + "_pkfUDqI5txWQIch3-BCki2bpw",
            "expirationTime": None,
            "keys": {
                "p256dh": "BH7z6g2qF6DHKPoJrR1C14ipaT2nhdOY-"
                + "FRZEkIM1XcCrWjyyZyyuaUg-BBPSlk2AI5-CYoeH7b0iOtmYGyTSYA",
                "auth": "8JKtxuSPDrHEoNrYqUewHQ",
            },
        },
        "ttl": 259200,
        "vapid_private_key": "f4oitY9xPckwPugvhvcubOMHaz-Wf1XM2IaPaLdN8lM",
        "vapid_claims": {"sub": "https://joynal.dev"},
        "data": json.dumps(
            {
                "title": "I came from demo",
                "launch_url": "https://joynal.dev",
                "priority": "normal",
                "options": {
                    "body": "Ignore it, it's a test notification",
                    "icon": "https://avatars3.githubusercontent.com/u/6458212",
                },
            }
        ),
    }

    webpush(**push_data)

except WebPushException as ex:
    print("I'm sorry, Dave, but I can't do that: {}", repr(ex))
    # Mozilla returns additional information in the body of the response.
    if ex.response and ex.response.json():
        extra = ex.response.json()
        print(
            "Remote service replied with a {}:{}, {}",
            extra.code,
            extra.errno,
            extra.message,
        )
