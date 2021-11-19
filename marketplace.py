import json
import requests

headers = {
    'authority': 'kawaii-martketplace-api.airight.io',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
    'content-type': 'application/json',
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'origin': 'https://kawaii-islands.airight.io',
    'referer': 'https://kawaii-islands.airight.io/',
}


def post(url, data):
    response = requests.post(url=url, data=data, headers=headers)
    return response


def options(url):
    response = requests.options(url=url, headers=headers)
    return response



def checkMarket():
    data = {
        "filters":{
            "limit":10,
            "sort":"CurrentPriceAsc",
            "category":"fields",
            "page":0,
            "marketplace":"0x48F49DB11db3D42B5aeAa3DFb084fC38CA469118"
        }
    }
    response = post('https://kawaii-martketplace-api.airight.io/v0/list_auction',json.dumps(data))

    for data in response:
        print(data)
                    
    # content = json.loads(response.content)
    # print(content)