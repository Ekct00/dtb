import requests

def wecom_send(key, title, content=""):
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}"
    data = {
        "msgtype": "markdown",
        "markdown": {
            "content": f"### {title}\n{content}"
        }
    }
    response = requests.post(url, json=data)
    return response.json()