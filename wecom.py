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


import base64
import hashlib

def wecom_send_image(key, image_data):
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}"
    
    # 计算图片的MD5值
    md5 = hashlib.md5(image_data).hexdigest()
    # Base64编码
    base64_data = base64.b64encode(image_data).decode('utf-8')
    
    data = {
        "msgtype": "image",
        "image": {
            "base64": base64_data,
            "md5": md5
        }
    }
    response = requests.post(url, json=data)
    return response.json()