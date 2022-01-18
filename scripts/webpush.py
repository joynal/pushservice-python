from pywebpush import webpush, WebPushException

try:
    webpush(
        subscription_info={
            "endpoint": "https://fcm.googleapis.com/fcm/send/cDCAWAwgfGg:APA91bHxr3sZVXFf6aEsd1DIYrVwbqo67bJb7H5whJPE5-rv3Og2jWbyB8Rh1P-pmuhiUvd3KnxLUSlGqhBnU52HdB3qtKquzBWetrHfm1uIplOynkv7kh17p7lE47aQgcEJOkz1f-iK",
            "expirationTime": None,
            "keys": {
                "p256dh": "BO8n7ZP5o7LpIoHXySJ79bArZwsVBj52_5ImzRZyJVAjWkL2qTE_YUaNYuJIoXJdwIAYlOYEH3eg8Lr92YHLTqk",
                "auth": "YzQw1LXXZQSY2Mzgd-JRcQ",
            },
        },
        # subscription_info={
        #     "endpoint": "https://fcm.googleapis.com/fcm/send/d2Vj2HXnWS0:APA91bGW_si_MDp8h2g016QAZIZy3w5jecWOn4ZB1oWX3qESi9ROlxfNc_QHSb_ELpzOGE5dRGwaa2M2rPGzFDZC63OV5962BH3747qg1bw2GkMVv3_pkfUDqI5txWQIch3-BCki2bpw",
        #     "expirationTime": None,
        #     "keys": {
        #         "p256dh": "BH7z6g2qF6DHKPoJrR1C14ipaT2nhdOY-FRZEkIM1XcCrWjyyZyyuaUg-BBPSlk2AI5-CYoeH7b0iOtmYGyTSYA",
        #         "auth": "8JKtxuSPDrHEoNrYqUewHQ"
        #     }
        # },
        data="Mary had a little lamb, with a nice mint jelly",
        vapid_private_key="f4oitY9xPckwPugvhvcubOMHaz-Wf1XM2IaPaLdN8lM",
        vapid_claims={
            "sub": "https://joynal.dev",
        },
    )

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
