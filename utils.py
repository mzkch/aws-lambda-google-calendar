import json
import urllib.request


def send_slack_message(webhook_url, pretext, title, message):
    headers = {"Content-type": "application/json"}
    data = {
        "attachments": [
            {
                "fallback": pretext,
                "pretext": pretext,
                "color": "#00ff7f",
                "fields": [
                    {
                        "title": title,
                        "value": message,
                        "short": False
                    }
                ]
            }
        ]
    }
    req = urllib.request.Request(
        webhook_url,
        data=json.dumps(data).encode("utf-8"),
        headers=headers
    )
    response = urllib.request.urlopen(req)
    return response.read().decode("utf-8")
