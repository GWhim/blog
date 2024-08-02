from hashlib import sha1
import hmac
import requests
import json
import urllib
import os

def dogecloud_api(api_path, data={}, json_mode=False):
    access_key = os.environ["ACCESS_KEY"]
    secret_key = os.environ["SECRET_KEY"]
    body = ''
    mime = ''
    if json_mode:
        body = json.dumps(data)
        mime = 'application/json'
    else:
        body = urllib.parse.urlencode(data) # Python 2 可以直接用 urllib.urlencode
        mime = 'application/x-www-form-urlencoded'
    sign_str = api_path + "\n" + body
    signed_data = hmac.new(secret_key.encode('utf-8'), sign_str.encode('utf-8'), sha1)
    sign = signed_data.digest().hex()
    authorization = 'TOKEN ' + access_key + ':' + sign
    response = requests.post('https://api.dogecloud.com' + api_path, data=body, headers = {
        'Authorization': authorization,
        'Content-Type': mime
    })
    return response.json()


url_list = [
    "https://blog.gwhim.cn/",
]

api = dogecloud_api('/cdn/refresh/add.json', {
    'rtype': 'path',
    'urls': json.dumps(url_list)
})
if api['code'] == 200:
    print(api['data']['task_id'])
else:
    print("api failed: " + api['msg']) # 失败